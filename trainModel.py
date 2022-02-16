"""Trains a model using all training data from a given szene"""

import numpy as np
import tensorflow as tf
import learned_simulator
import noise_utils
import time
import createTrainingsDatasets

SEQUENCE_LENGTH = 5
NUM_DIMENSIONS = 2
NUM_PARTICLE_TYPES = 2
NUM_STOPPER = 4
NUM_PATRICLES_PER_STOPPER = 40
NUM_BOUNDARY_PARTICLES = NUM_PATRICLES_PER_STOPPER*NUM_STOPPER
NUM_CARGO_PARTICLES = 35

BATCH_SIZE = 1
GLOBAL_CONTEXT_SIZE = 1

NOISE_STD = np.float32(4e-5)
CONNECTIVITY_RADIUS = 0.2

DATA_REPETITIONS = 4

MIN_LR = 1e-5
MAX_LR = 1e-4
LR_STEPS = 2e5

DATA_PATH = "Data/Numpy/Szene1"
MODEL_PATH = "Models/Szene1"
NUM_STEPS = 2e7
KINEMATIC_PARTICLE_ID = 1
BOUNDARIES = [(0,1),(0,np.float32(6))]

def main():
    start = time.perf_counter()
    print("Start: " + str(start))
    tf.logging.set_verbosity(tf.logging.INFO)
    estimator = tf.estimator.Estimator(
        get_one_step_estimator_fn(NOISE_STD),model_dir=MODEL_PATH)
    input_fn=get_input_fn()
    data = time.perf_counter()
    estimator.train(
         input_fn ,max_steps=NUM_STEPS)
    stop = time.perf_counter()
    print("Start: " + str(start))
    print("Read data: " + str(data))
    print("Stop: " + str(stop))

    print("Time to read data: " + str(data-start))
    print("Time to train: " + str(stop-data))


def get_kinematic_mask(particle_types):
  """Returns a boolean mask, set to true for kinematic (obstacle) particles."""
  return tf.equal(particle_types, KINEMATIC_PARTICLE_ID)


def get_input_fn():
  """Gets the learning simulation input function for tf.estimator.Estimator.
  Returns:
    The input function for the learning simulation model.
  """
  def input_fn():
    # Get datasets as NumPy Arrays
    train_examples = np.empty(shape=(1,SEQUENCE_LENGTH+1,NUM_BOUNDARY_PARTICLES+NUM_CARGO_PARTICLES,NUM_DIMENSIONS),dtype=np.float32)
    train_labels = np.empty(shape=(1,NUM_BOUNDARY_PARTICLES+NUM_CARGO_PARTICLES,NUM_DIMENSIONS),dtype=np.float32)
    train_examples, train_labels = createTrainingsDatasets.getTrainingDatasetsSzene1(train_examples, train_labels)

    # Convert datasets to tf Tensors of the desired shape
    train_examples = train_examples.transpose([0,2,1,3])
    #filename = 'TrainingDataExamples'
    #with open(DATA_PATH+'/'+filename + '.npy', 'rb') as f:
    #    train_examples = np.load(f)
    #filename = 'TrainingDataLabels'
    #with open(DATA_PATH+'/'+filename + '.npy', 'rb') as f:
    #    train_labels = np.load(f)

    train_examples = tf.convert_to_tensor(train_examples[1:], dtype = tf.float32)
    train_labels =  tf.convert_to_tensor(train_labels[1:], dtype = tf.float32)
    train_dataset = tf.data.Dataset.from_tensor_slices((train_examples,train_labels))
    
    # Repeat and randomly shuffle dataset
    train_dataset = train_dataset.repeat(DATA_REPETITIONS)
    train_dataset = train_dataset.shuffle(300)

    return train_dataset

  return input_fn


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

def get_one_step_estimator_fn(noise_std):
    """Gets one step model for training simulation."""
    # Sets NN structure
    model_kwargs = dict(
        latent_size=64,
        mlp_hidden_size=64,
        mlp_num_hidden_layers=2,
        num_message_passing_steps=10)
    def estimator_fn(features, labels, mode):
        target_next_position = labels
        simulator = _get_simulator(model_kwargs)
        input_position_sequence = features

        # Sample the noise to add to the inputs to the model during training.
        sampled_noise = noise_utils.get_random_walk_noise_for_position_sequence(
            input_position_sequence, noise_std_last_step=noise_std)

        # Sets cargo particles to type 0 and obstacle particles to type 1
        particle_types = np.transpose(np.hstack((np.zeros(shape=(NUM_DIMENSIONS,NUM_CARGO_PARTICLES)),np.ones(shape=(NUM_DIMENSIONS,NUM_BOUNDARY_PARTICLES))*1)))
        particle_types = tf.convert_to_tensor(particle_types, dtype = tf.int64)

        # sets global_context to 0
        global_context = tf.zeros([BATCH_SIZE, GLOBAL_CONTEXT_SIZE], dtype=tf.float32)

        # sets number of particles
        n_particles_per_example = tf.convert_to_tensor([NUM_BOUNDARY_PARTICLES+NUM_CARGO_PARTICLES], dtype = np.int32)

        # Get the predictions and target velocities.
        pred_target = simulator.get_predicted_and_target_velocities(
                target_next_position, sampled_noise,
                input_position_sequence, n_particles_per_example, global_context, particle_types[:,0])
        pred_velocity, target_velocity, _, _ = pred_target

        # Sets loss funktion, learning rate and optimizer
        loss = (pred_velocity[0:NUM_CARGO_PARTICLES] - target_velocity[0:NUM_CARGO_PARTICLES])**2
        loss = tf.reduce_sum(loss) 
        global_step = tf.train.get_global_step()
        lr = tf.train.exponential_decay(learning_rate=MAX_LR - MIN_LR,
                                        global_step=global_step,
                                        decay_steps=int(LR_STEPS),
                                        decay_rate=0.1) + MIN_LR
        opt = tf.train.AdamOptimizer(learning_rate=lr)
        train_op = opt.minimize(loss, global_step)

        # Predicts position of next step
        predicted_next_position = simulator(input_position_sequence, n_particles_per_example, global_context, particle_types[:,0])
        predictions = {'predicted_next_position': predicted_next_position}
        
        # Sets log
        logging_hook = tf.train.LoggingTensorHook({
        "pred_velocity" : pred_velocity[0:NUM_CARGO_PARTICLES]*10000, "target_velocity" : target_velocity[0:NUM_CARGO_PARTICLES]*10000, "_loss" : loss*1000000000}, every_n_iter=50)
        eval_metrics_ops = {
            'loss_mse': tf.metrics.mean_squared_error(
                pred_velocity, target_velocity),
            'one_step_position_mse': tf.metrics.mean_squared_error(
                predicted_next_position, target_next_position)
        }
        return tf.estimator.EstimatorSpec(
            mode=mode,
            train_op=train_op,
            loss=loss,
            predictions=predictions,
            eval_metric_ops=eval_metrics_ops,
            training_hooks = [logging_hook])
    return estimator_fn 

def readData(data, num_particles):
    """Gets all positions from the dataset data"""
    positions = np.empty(shape=(1,num_particles,NUM_DIMENSIONS),dtype=np.float32)
    for i in range(data.shape[0]):
        pos = getPositions(data,i,num_particles)[None]
        positions = np.vstack((positions,pos))
    return positions[1:]

def getPositions(data, i, num_particles):
    """Gets the position matrix of the dataset data at position i"""
    positionData = np.empty(shape=(1,NUM_DIMENSIONS),dtype=np.float32)
    for j in range(NUM_DIMENSIONS*num_particles):
        if(j%NUM_DIMENSIONS == 0):
            positionData = np.vstack((positionData, [data[i][j],data[i][j+1]]))
    return positionData[1:]

if __name__ == "__main__":
    tf.disable_v2_behavior()
    main()

