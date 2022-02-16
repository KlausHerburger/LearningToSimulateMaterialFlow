"""Full model implementation """

import graph_nets as gn
import sonnet as snt
import tensorflow as tf

import connectivity_utils
import graph_network


class LearnedSimulator(snt.AbstractModule):
  """Learned simulator"""

  def __init__(
      self,
      num_dimensions,
      connectivity_radius,
      graph_network_kwargs,
      boundaries,
      num_particle_types,
      particle_type_embedding_size,
      num_particles,
      name="LearnedSimulator"):
    """Inits the model.
    Args:
      num_dimensions: Dimensionality of the problem.
      connectivity_radius: Scalar with the radius of connectivity.
      graph_network_kwargs: Keyword arguments to pass to the learned part
        of the graph network `model.EncodeProcessDecode`.
      boundaries: List of 2-tuples, containing the lower and upper boundaries of
        the cuboid containing the particles along each dimensions, matching
        the dimensionality of the szene.
      num_particle_types: Number of different particle types.
      particle_type_embedding_size: Embedding size for the particle type.
      num_particles: Number of particles in the szene.
      name: Name of the Sonnet module.
    """
    super().__init__(name=name)

    self._connectivity_radius = connectivity_radius
    self._num_particle_types = num_particle_types
    self._num_particles = num_particles
    self._boundaries = boundaries
    with self._enter_variable_scope():
      self._graph_network = graph_network.EncodeProcessDecode(
          output_size=num_dimensions, **graph_network_kwargs)

      if self._num_particle_types > 1:
        self._particle_type_embedding = tf.get_variable(
            "particle_embedding",
            [self._num_particle_types, particle_type_embedding_size],
            trainable=True, use_resource=True)

  def _build(self, position_sequence, n_particles_per_example,
             global_context=None, particle_types=None):
    """Produces a model step, outputting the next position for each particle.
    Args:
      position_sequence: Sequence of positions for each node in the batch,
        with shape [num_particles_in_batch, sequence_length, num_dimensions]
      n_particles_per_example: Number of particles for each graph
      global_context: Tensor of shape [batch_size, context_size], with global
        context.
      particle_types: Integer tensor of shape [num_particles_in_batch] with
        the integer types of the particles, from 0 to `num_particle_types - 1`.
        If None, we assume all particles are the same type.
    Returns:
      Next position with shape [num_particles_in_batch, num_dimensions] for one
      step into the future from the input sequence.
    """
    input_graphs_tuple = self._encoder_preprocessor(
        position_sequence, n_particles_per_example, global_context,
        particle_types)

    velocity = self._graph_network(input_graphs_tuple)

    next_position = self._decoder_postprocessor(
        velocity, position_sequence)

    return next_position

  def _encoder_preprocessor(
      self, position_sequence, n_node, global_context, particle_types):
    # Extract important features from the position_sequence.
    most_recent_position = position_sequence[:, -1]
    velocity_sequence = time_diff(position_sequence)  # Finite-difference.

    # Get connectivity of the graph.
    (senders, receivers, n_edge) = connectivity_utils.compute_connectivity_for_batch_pyfunc(
         most_recent_position, n_node, self._connectivity_radius)

    # Collect node features.
    node_features = []

    flat_velocity_sequence = snt.MergeDims(start=1, size=2)(velocity_sequence)
    node_features.append(flat_velocity_sequence)

    # Normalized clipped distances to lower and upper boundaries.
    # boundaries are an array of shape [num_dimensions, 2], where the second
    # axis, provides the lower/upper boundaries.
    boundaries = tf.constant(self._boundaries, dtype=tf.float32)
    distance_to_lower_boundary = (
        most_recent_position - tf.expand_dims(boundaries[:, 0], 0))
    distance_to_upper_boundary = (
        tf.expand_dims(boundaries[:, 1], 0) - most_recent_position)
    distance_to_boundaries = tf.concat(
        [distance_to_lower_boundary, distance_to_upper_boundary], axis=1)
    normalized_clipped_distance_to_boundaries = tf.clip_by_value(
        distance_to_boundaries / self._connectivity_radius, -1., 1.)
    node_features.append(normalized_clipped_distance_to_boundaries)

    # Particle type.
    if self._num_particle_types > 1:
      particle_type_embeddings = tf.nn.embedding_lookup(
          self._particle_type_embedding, particle_types)
      particle_type_embeddings = tf.reshape(particle_type_embeddings, [self._num_particles,16])
      node_features.append(particle_type_embeddings)

    # Collect edge features.
    edge_features = []

    # Relative displacement and distances normalized to radius
    normalized_relative_displacements = (
        tf.gather(most_recent_position, senders) -
        tf.gather(most_recent_position, receivers)) / self._connectivity_radius
    edge_features.append(normalized_relative_displacements)

    normalized_relative_distances = tf.norm(
        normalized_relative_displacements, axis=-1, keepdims=True)
    edge_features.append(normalized_relative_distances)

    return gn.graphs.GraphsTuple(
        nodes=tf.concat(node_features, axis=-1),
        edges=tf.concat(edge_features, axis=-1),
        globals=global_context,  # self._graph_net will appending this to nodes.
        n_node=n_node,
        n_edge=n_edge,
        senders=senders,
        receivers=receivers,
        )

  def _decoder_postprocessor(self, velocity, position_sequence):
    # Use an Euler integrator to go from velocity to position, assuming
    # a dt=1 corresponding to the size of the finite difference.
    most_recent_position = position_sequence[:, -1]
    dt = 1
    new_position = most_recent_position + velocity*dt 
    return new_position

  def get_predicted_and_target_velocities(
      self, next_position, position_sequence_noise, position_sequence,
      n_particles_per_example, global_context=None, particle_types=None):  
    """Produces predicted velocity targets.
    Args:
      next_position: Tensor of shape [num_particles_in_batch, num_dimensions]
        with the positions the model should output given the inputs.
      position_sequence_noise: Tensor of the same shape as `position_sequence`
        with the noise to apply to each particle.
      position_sequence, n_node, global_context, particle_types: Inputs to the
        model as defined by `_build`.
    Returns:
      Tensors of shape [num_particles_in_batch, num_dimensions] with the
        predicted and target velcoties.
    """

    # Add noise to the input position sequence.
    noisy_position_sequence = position_sequence + position_sequence_noise

    # Perform the forward pass with the noisy position sequence.
    input_graphs_tuple = self._encoder_preprocessor(
        noisy_position_sequence, n_particles_per_example, global_context,
        particle_types)
    predicted_velocity = self._graph_network(input_graphs_tuple)

    # Calculate the target velocity, using an `adjusted_next_position `that
    # is shifted by the noise in the last input position.
    next_position_adjusted = next_position + position_sequence_noise[:, -1]
    target_velocity = self._inverse_decoder_postprocessor(
        next_position_adjusted, noisy_position_sequence)

    return predicted_velocity, target_velocity, input_graphs_tuple.senders, input_graphs_tuple.receivers

  def _inverse_decoder_postprocessor(self, next_position, position_sequence):
    """Inverse of `_decoder_postprocessor`."""

    previous_position = position_sequence[:, -1]
    next_velocity = next_position - previous_position

    return next_velocity


def time_diff(input_sequence):
  return input_sequence[:, 1:] - input_sequence[:, :-1]