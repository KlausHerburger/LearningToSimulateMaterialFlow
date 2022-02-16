"""Evaluates a model for a given szene by generating rollouts with the validation data"""

from absl import app
import numpy as np
import tensorflow as tf
from scipy import io
import tree
import learned_simulator
import trainModel
import time

SEQUENCE_LENGTH = 5
NUM_DIMENSIONS = 2
NUM_PARTICLE_TYPES = 2
NUM_STOPPER = 5
NUM_PATRICLES_PER_STOPPER = 40
NUM_BOUNDARY_PARTICLES = NUM_PATRICLES_PER_STOPPER*NUM_STOPPER
NUM_CARGO_PARTICLES = 9
BATCH_SIZE = 1
GLOBAL_CONTEXT_SIZE = 1

CONNECTIVITY_RADIUS = 0.15
EVERY_N = 5

MODEL_PATH = "Models/Szene1"
DATA_PATH = 'Data/Numpy/Szene1'
OUTPUT_PATH = "Rollouts/Szene1//"
KINEMATIC_PARTICLE_ID = 1
BOUNDARIES = [(0,1),(0,np.float32(6))]

ANGLE1 = 60
ANGLE2 = 60
ANGLE3 = 70
ANGLE4 = 70
VERSION = 1
#FILENAME = str(ANGLE1) + '_' + str(ANGLE2) + '_' + str(VERSION) + '_' + str(NUM_CARGO_PARTICLES)
FILENAME = 'Gen_' + str(ANGLE1) + '_' + str(ANGLE2) + '_' + str(ANGLE3) + '_' + str(ANGLE4) + '_' + str(VERSION) + '_' + str(NUM_CARGO_PARTICLES)


def get_kinematic_mask(particle_types):
  """Returns a boolean mask, set to true for kinematic (obstacle) particles."""
  return tf.equal(particle_types, KINEMATIC_PARTICLE_ID)

def get_input_fn():
    def input_fn():
        # Get NumPy dataset for evaluation
        angle1=ANGLE1*np.pi/180
        angle2=ANGLE2*np.pi/180
        angle3=ANGLE3*np.pi/180
        angle4=ANGLE4*np.pi/180

        # Convert datasets to tf Tensors of the desired shape
        test_examples, test_labels = getGeneralisationDatasetSzene3(angle1, angle2, angle3, angle4)
        test_examples = tf.convert_to_tensor(test_examples[1:,:,:,:].transpose([1,2,0,3]), dtype = tf.float32)
        test_labels =  tf.convert_to_tensor(test_labels[1:], dtype = tf.float32)
        test_dataset = tf.data.Dataset.from_tensor_slices((test_examples,test_labels))
        return test_dataset

    return input_fn()

def getTestDatasetSzene1(angle1):
    """Read the evaluation dataset for Szene1"""
    test_examples = np.empty(shape=(1,1,NUM_BOUNDARY_PARTICLES+NUM_CARGO_PARTICLES,NUM_DIMENSIONS),dtype=np.float32)
    test_labels = np.empty(shape=(1,NUM_BOUNDARY_PARTICLES+NUM_CARGO_PARTICLES,NUM_DIMENSIONS),dtype=np.float32)
    # read dataset
    with open(DATA_PATH+'/'+FILENAME+'.npy', 'rb') as f:
        a = np.load(f)
    data = trainModel.readData(a, NUM_CARGO_PARTICLES)

    # add positions of stopper-elements
    obstacle_positions = np.empty(shape=(1,NUM_DIMENSIONS))
    for i in np.linspace(-10,10,NUM_PATRICLES_PER_STOPPER):
        obstacle_positions = np.vstack((obstacle_positions,[0.24+np.cos(angle1)*0.35*i/10, 1.47+np.sin(angle1)*0.35*i/10]))
    obstacle_positions = obstacle_positions[1:]
    k = EVERY_N #take every k-th position of dataset

    # loop through all positions
    for i in range(int((len(data))-k-1)):
        if i%k == 0:
            test_examples = np.vstack((test_examples,np.hstack((data[[i],:],obstacle_positions[None]))[None]))
    test_labels = np.vstack((test_labels,np.hstack((data[[i+1],:],obstacle_positions[None]))))
    return test_examples, test_labels

def getTestDatasetSzene2(angle1):
    """Read the evaluation dataset for Szene2"""
    test_examples = np.empty(shape=(1,1,NUM_BOUNDARY_PARTICLES+NUM_CARGO_PARTICLES,NUM_DIMENSIONS),dtype=np.float32)
    test_labels = np.empty(shape=(1,NUM_BOUNDARY_PARTICLES+NUM_CARGO_PARTICLES,NUM_DIMENSIONS),dtype=np.float32)
    # read dataset
    with open(DATA_PATH+'/'+FILENAME+'.npy', 'rb') as f:
        a = np.load(f)
    data = trainModel.readData(a, NUM_CARGO_PARTICLES)

    # add positions of stopper-elements
    obstacle_positions = np.empty(shape=(1,NUM_DIMENSIONS))
    for i in np.linspace(-10,10,NUM_PATRICLES_PER_STOPPER):
        obstacle_positions = np.vstack((obstacle_positions,[0.24+np.cos(angle1)*0.35*i/10, 1.47+np.sin(angle1)*0.35*i/10]))
    for i in np.linspace(0,1,NUM_PATRICLES_PER_STOPPER):
        obstacle_positions = np.vstack((obstacle_positions,[i, 3]))
    obstacle_positions = obstacle_positions[1:]
    k = EVERY_N #take every k-th position of dataset

    # loop through all positions
    for i in range(int((len(data))-k-1)):
        if i%k == 0:
            test_examples = np.vstack((test_examples,np.hstack((data[[i],:],obstacle_positions[None]))[None]))
    test_labels = np.vstack((test_labels,np.hstack((data[[i+1],:],obstacle_positions[None]))))
    return test_examples, test_labels

def getTestDatasetSzene3(angle1, angle2):
    """Read the evaluation dataset a for Szene3"""
    test_examples = np.empty(shape=(1,1,NUM_BOUNDARY_PARTICLES+NUM_CARGO_PARTICLES,NUM_DIMENSIONS),dtype=np.float32)
    test_labels = np.empty(shape=(1,NUM_BOUNDARY_PARTICLES+NUM_CARGO_PARTICLES,NUM_DIMENSIONS),dtype=np.float32)
    # read dataset
    with open(DATA_PATH+'/'+FILENAME+'.npy', 'rb') as f:
        a = np.load(f)
    data = trainModel.readData(a, NUM_CARGO_PARTICLES)

    # add positions of stopper-elements
    obstacle_positions = np.empty(shape=(1,NUM_DIMENSIONS))
    for i in np.linspace(-10,10,NUM_PATRICLES_PER_STOPPER):
        obstacle_positions = np.vstack((obstacle_positions,[0.24+np.cos(angle1)*0.35*i/10, 1.47+np.sin(angle1)*0.35*i/10]))
    for i in np.linspace(-10,10,NUM_PATRICLES_PER_STOPPER):
        obstacle_positions = np.vstack((obstacle_positions,[0.65+np.cos(-angle2)*0.5*i/10, 3+np.sin(-angle2)*0.5*i/10]))
    for i in np.linspace(0,1,NUM_PATRICLES_PER_STOPPER):
        obstacle_positions = np.vstack((obstacle_positions,[i, 6]))
    obstacle_positions = obstacle_positions[1:]
    k = EVERY_N #take every k-th position of dataset

    # loop through all positions
    for i in range(int((len(data))-k-1)):
        if i%k == 0:
            test_examples = np.vstack((test_examples,np.hstack((data[[i],:],obstacle_positions[None]))[None]))
    test_labels = np.vstack((test_labels,np.hstack((data[[i+1],:],obstacle_positions[None]))))
    return test_examples, test_labels


def getGeneralisationDatasetSzene3(angle1, angle2, angle3, angle4):
    """Read the generalisation evaluation dataset for Szene3"""
    test_examples = np.empty(shape=(1,1,NUM_BOUNDARY_PARTICLES+NUM_CARGO_PARTICLES,NUM_DIMENSIONS),dtype=np.float32)
    test_labels = np.empty(shape=(1,NUM_BOUNDARY_PARTICLES+NUM_CARGO_PARTICLES,NUM_DIMENSIONS),dtype=np.float32)
    # read dataset
    with open(DATA_PATH+'/'+FILENAME+'.npy', 'rb') as f:
        a = np.load(f)
    data = trainModel.readData(a, NUM_CARGO_PARTICLES)

    # add positions of stopper-elements
    obstacle_positions = np.empty(shape=(1,NUM_DIMENSIONS))
    for i in np.linspace(-10,10,NUM_PATRICLES_PER_STOPPER):
        obstacle_positions = np.vstack((obstacle_positions,[0.24+np.cos(angle1)*0.35*i/10, 1.47+np.sin(angle1)*0.35*i/10]))
    for i in np.linspace(-10,10,NUM_PATRICLES_PER_STOPPER):
        obstacle_positions = np.vstack((obstacle_positions,[0.76+np.cos(-angle2)*0.35*i/10, 2.5+np.sin(-angle2)*0.35*i/10]))
    for i in np.linspace(-10,10,NUM_PATRICLES_PER_STOPPER):
        obstacle_positions = np.vstack((obstacle_positions,[0.2+np.cos(angle3)*0.5*i/10, 4+np.sin(angle3)*0.5*i/10]))
    for i in np.linspace(-10,10,NUM_PATRICLES_PER_STOPPER):
        obstacle_positions = np.vstack((obstacle_positions,[0.8+np.cos(-angle4)*0.5*i/10, 4+np.sin(-angle4)*0.5*i/10]))
    for i in np.linspace(0,1,NUM_PATRICLES_PER_STOPPER):
        obstacle_positions = np.vstack((obstacle_positions,[i, 6]))
    obstacle_positions = obstacle_positions[1:]
    k = EVERY_N #take every k-th position of dataset

    # loop through all positions
    for i in range(int((len(data))-k-1)):
        if i%k == 0:
            test_examples = np.vstack((test_examples,np.hstack((data[[i],:],obstacle_positions[None]))[None]))
    test_labels = np.vstack((test_labels,np.hstack((data[[i+1],:],obstacle_positions[None]))))
    return test_examples, test_labels

def rollout(simulator, features, num_steps):
    # Sets cargo particles to type 0 and obstacle particles to type 1
    particle_types = np.transpose(np.hstack((np.zeros(shape=(NUM_DIMENSIONS,NUM_CARGO_PARTICLES)),np.ones(shape=(NUM_DIMENSIONS,NUM_BOUNDARY_PARTICLES))*1)))
    particle_types = tf.convert_to_tensor(particle_types, dtype = tf.int64)

    # Reads initial positions for the rollout, ground_truth postitions and sets global_context
    initial_positions = features[:,0:(SEQUENCE_LENGTH+1)]
    ground_truth_positions = features[:,(SEQUENCE_LENGTH+1):]
    global_context = tf.zeros([BATCH_SIZE, GLOBAL_CONTEXT_SIZE], dtype=tf.float32)

    def step_fn(step, current_positions, predictions):
        """Simulats one step"""
        n_particles_per_example = tf.convert_to_tensor([NUM_CARGO_PARTICLES+NUM_BOUNDARY_PARTICLES], dtype = np.int32)
        next_position = simulator(current_positions, n_particles_per_example, global_context, particle_types[:,0])

        kinematic_mask = get_kinematic_mask(particle_types)
        next_position_ground_truth = ground_truth_positions[:, step]
        next_position = tf.where(kinematic_mask, next_position_ground_truth,
                                next_position)
        updated_predictions = predictions.write(step, next_position)

        # Shift `current_positions`, removing the oldest position in the sequence
        # and appending the next position at the end.
        next_positions = tf.concat([current_positions[:, 1:],
                                    next_position[:, tf.newaxis]], axis=1)

        return (step + 1, next_positions, updated_predictions)

    start = time.perf_counter()
    predictions = tf.TensorArray(size=num_steps, dtype=tf.float32)
    _, _, predictions = tf.while_loop(
        cond=lambda step, state, prediction: tf.less(step, num_steps),
        body=step_fn,
        loop_vars=(0, initial_positions, predictions),
        back_prop=False,
        parallel_iterations=1)
    
    stop = time.perf_counter()

    output_dict = {
        'initial_positions': tf.transpose(initial_positions, [1, 0, 2]),
        'predicted_rollout': predictions.stack(),
        'ground_truth_rollout': tf.transpose(ground_truth_positions, [1, 0, 2]),
        'particle_types': particle_types,
        'time' : tf.cast(stop-start, dtype=np.float32)
    }

    if global_context is not None:
        output_dict['global_context'] = global_context
    return output_dict


def _get_simulator(model_kwargs):
    """Instantiates the simulator."""
    simulator = learned_simulator.LearnedSimulator(
        num_dimensions=NUM_DIMENSIONS,
        connectivity_radius=np.float32(CONNECTIVITY_RADIUS),
        graph_network_kwargs=model_kwargs,
        boundaries=BOUNDARIES,
        num_particle_types=NUM_PARTICLE_TYPES,
        particle_type_embedding_size=16,
        num_particles = NUM_BOUNDARY_PARTICLES+NUM_CARGO_PARTICLES)
    return simulator

def get_rollout_estimator_fn(latent_size=64,
                             hidden_size=64,
                             hidden_layers=2,
                             message_passing_steps=10):
  """Gets the model function for tf.estimator.Estimator."""
  model_kwargs = dict(
      latent_size=latent_size,
      mlp_hidden_size=hidden_size,
      mlp_num_hidden_layers=hidden_layers,
      num_message_passing_steps=message_passing_steps)

  def estimator_fn(features, labels, mode):
    del labels  # Labels to conform to estimator spec.
    simulator = _get_simulator(model_kwargs)
    num_steps = features.get_shape().as_list()[1] - (SEQUENCE_LENGTH+1) #set number of rollout steps equal to testdataset length
    rollout_op = rollout(simulator, features, num_steps=num_steps)
    squared_error = (rollout_op['predicted_rollout'] -
                     rollout_op['ground_truth_rollout']) ** 2
    loss = tf.reduce_mean(squared_error)
    eval_ops = {'rollout_error_mse': tf.metrics.mean_squared_error(
        rollout_op['predicted_rollout'], rollout_op['ground_truth_rollout'])}

    # Add a leading axis, since Estimator's predict method insists that all
    # tensors have a shared leading batch axis fo the same dims.
    rollout_op = tree.map_structure(lambda x: x[tf.newaxis], rollout_op)
    return tf.estimator.EstimatorSpec(
        mode=mode,
        train_op=None,
        loss=loss,
        predictions=rollout_op,
        eval_metric_ops=eval_ops)

  return estimator_fn


def main(_):
    rollout_estimator = tf.estimator.Estimator(
        get_rollout_estimator_fn(),
        model_dir=MODEL_PATH)
    rollout_iterator = rollout_estimator.predict(
        input_fn=get_input_fn)
    for example_index, example_rollout in enumerate(rollout_iterator):

        n = open(OUTPUT_PATH+FILENAME+'.npy', 'wb')
        m = open(OUTPUT_PATH+FILENAME+'.mat', 'wb')
        rollout = example_rollout['predicted_rollout'].reshape(example_rollout['predicted_rollout'].shape[0],NUM_DIMENSIONS*(NUM_BOUNDARY_PARTICLES+NUM_CARGO_PARTICLES))
        true_rollout = example_rollout['ground_truth_rollout'].reshape(example_rollout['ground_truth_rollout'].shape[0],2*(NUM_BOUNDARY_PARTICLES+NUM_CARGO_PARTICLES))
        error = np.mean(np.linalg.norm(true_rollout[:,0:2*NUM_CARGO_PARTICLES].reshape(true_rollout.shape[0],NUM_CARGO_PARTICLES,NUM_DIMENSIONS)-rollout[:,0:2*NUM_CARGO_PARTICLES].reshape(true_rollout.shape[0],NUM_CARGO_PARTICLES,NUM_DIMENSIONS),axis=2))
        np.save(n, rollout)
        io.savemat(m, {'data_rollout': rollout, 'true_rollout': true_rollout, 'error' : error, 'time': example_rollout['time']})



if __name__ == '__main__':
  tf.disable_v2_behavior()
  app.run(main)