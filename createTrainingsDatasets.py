"""Creates training datasets with all training data in one array for a given Szene"""

import numpy as np
import tensorflow as tf
import trainModel

SEQUENCE_LENGTH = 5
NUM_DIMENSIONS = 2
NUM_PARTICLE_TYPES = 2
NUM_STOPPER = 4
NUM_PATRICLES_PER_STOPPER = 40
NUM_BOUNDARY_PARTICLES = NUM_PATRICLES_PER_STOPPER*NUM_STOPPER
NUM_CARGO_PARTICLES = 35

EVERY_N = 4
DATA_PATH = "Data/Numpy/Szene1"


def main():
    """Create dataset for given Szene"""
    train_examples = np.empty(shape=(1,SEQUENCE_LENGTH+1,NUM_BOUNDARY_PARTICLES+NUM_CARGO_PARTICLES,NUM_DIMENSIONS),dtype=np.float32)
    train_labels = np.empty(shape=(1,NUM_BOUNDARY_PARTICLES+NUM_CARGO_PARTICLES,NUM_DIMENSIONS),dtype=np.float32)
    train_examples, train_labels = getTrainingDatasetsSzene1(train_examples, train_labels)

    # Convert datasets to tf Tensors of the desired shape
    train_examples = train_examples.transpose([0,2,1,3])
    n = (open(DATA_PATH + '/' + "TrainingDataLabels" + '.npy', 'wb'))
    np.save(n, train_labels)
    n = (open(DATA_PATH + '/' + "TrainingDataExamples" + '.npy', 'wb'))
    np.save(n, train_examples)


def getTrainingDatasetsSzene1(train_examples, train_labels):
    """ Read all training datasets for Szene1

    Args:
        train_examples: emtpy array with correct shape to write examples to
        train_labels: emtpy array with correct shape to write labels to

    Returns:
        train_examples: array with all examples
        train_labels: array with all labels
    """

    # loop through all datasets
    for angle1_deg in range(31):
        angle1=(angle1_deg+30)*np.pi/180
        # add positions of stopper-elements
        obstacle_positions = np.empty(shape=(1,NUM_DIMENSIONS))
        for i in np.linspace(-10,10,NUM_PATRICLES_PER_STOPPER):
            obstacle_positions = np.vstack((obstacle_positions,[0.24+np.cos(angle1)*0.35*i/10, 1.47+np.sin(angle1)*0.35*i/10]))
        obstacle_positions = obstacle_positions[1:]
        
        # loop through all starting positions
        for version in [1,2,3]:
            if(not(angle1_deg==30 and version==1) or (angle1_deg==33 and version==2) or (angle1_deg==37 and version==3) or (angle1_deg==41 and version==1) or (angle1_deg==45 and version==2) or (angle1_deg==49 and version==3) or (angle1_deg==53 and version==1) or (angle1_deg==57 and version==2) or (angle1_deg==60 and version==3)):
                filename = str(angle1_deg+30) + '_' + str(version) 
                print(filename)
                with open(DATA_PATH+'/'+filename + '.npy', 'rb') as f:
                    datanpy = np.load(f)
                data = trainModel.readData(datanpy, NUM_CARGO_PARTICLES)
                k = EVERY_N #take every k-th position of dataset

                # loop through all positions
                for i in range(int((len(data))-7*k)):
                    train_data = np.vstack((np.hstack((data[[i],:],obstacle_positions[None])),np.hstack((data[[i+k],:],obstacle_positions[None])),np.hstack((data[[i+2*k],:],obstacle_positions[None])),np.hstack((data[[i+3*k],:],obstacle_positions[None])),np.hstack((data[[i+4*k],:],obstacle_positions[None])),np.hstack((data[[i+5*k],:],obstacle_positions[None]))))
                    train_examples = np.vstack((train_examples,train_data[None]))
                    train_labels = np.vstack((train_labels,np.hstack((data[[i+6*k],:],obstacle_positions[None]))))

    return train_examples, train_labels

def getTrainingDatasetsSzene2(train_examples, train_labels):
        """ Read all training datasets for Szene2

    Args:
        train_examples: emtpy array with correct shape to write examples to
        train_labels: emtpy array with correct shape to write labels to

    Returns:
        train_examples: array with all examples
        train_labels: array with all labels
    """

    # loop through all datasets
    for angle1_deg in range(31):
        angle1=(angle1_deg+30)*np.pi/180

        # add positions of stopper-elements
        obstacle_positions = np.empty(shape=(1,NUM_DIMENSIONS))
        for i in np.linspace(-10,10,NUM_PATRICLES_PER_STOPPER):
            obstacle_positions = np.vstack((obstacle_positions,[0.24+np.cos(angle1)*0.35*i/10, 1.47+np.sin(angle1)*0.35*i/10]))
        for i in np.linspace(0,1,NUM_PATRICLES_PER_STOPPER):
            obstacle_positions = np.vstack((obstacle_positions,[i, 3]))
        obstacle_positions = obstacle_positions[1:]
        
        # loop throug all starting positions
        for version in [1,2,3]:
            if(not(angle1_deg==30 and version==1) or (angle1_deg==33 and version==2) or (angle1_deg==37 and version==3) or (angle1_deg==41 and version==1) or (angle1_deg==45 and version==2) or (angle1_deg==49 and version==3) or (angle1_deg==53 and version==1) or (angle1_deg==57 and version==2) or (angle1_deg==60 and version==3)):
                filename = str(angle1_deg+30) + '_'  + str(version)
                print(filename)
                with open(DATA_PATH+'/'+filename + '_9.npy', 'rb') as f:
                    datanpy = np.load(f)
                data = trainModel.readData(datanpy, NUM_CARGO_PARTICLES)
                k = EVERY_N #take every k-th position of dataset

                # loop through all positions
                for i in range(int((len(data))-7*k)):
                    train_data = np.vstack((np.hstack((data[[i],:],obstacle_positions[None])),np.hstack((data[[i+k],:],obstacle_positions[None])),np.hstack((data[[i+2*k],:],obstacle_positions[None])),np.hstack((data[[i+3*k],:],obstacle_positions[None])),np.hstack((data[[i+4*k],:],obstacle_positions[None])),np.hstack((data[[i+5*k],:],obstacle_positions[None]))))
                    train_examples = np.vstack((train_examples,train_data[None]))
                    train_labels = np.vstack((train_labels,np.hstack((data[[i+6*k],:],obstacle_positions[None]))))
    return train_examples, train_labels


def getTrainingDatasetsSzene3(train_examples, train_labels):
    """ Read all training datasets for Szene3

    Args:
        train_examples: emtpy array with correct shape to write examples to
        train_labels: emtpy array with correct shape to write labels to

    Returns:
        train_examples: array with all examples
        train_labels: array with all labels
    """

    # loop through all datasets
    for angle1_deg in range(7):
        angle1=(angle1_deg*5+30)*np.pi/180
        for angle2_deg in range(4):
            angle2=(angle2_deg*5+45)*np.pi/180

            # add positions of stopper-elements
            obstacle_positions = np.empty(shape=(1,NUM_DIMENSIONS))
            for i in np.linspace(-10,10,NUM_PATRICLES_PER_STOPPER):
                obstacle_positions = np.vstack((obstacle_positions,[0.24+np.cos(angle1)*0.35*i/10, 1.47+np.sin(angle1)*0.35*i/10]))
            for i in np.linspace(-10,10,NUM_PATRICLES_PER_STOPPER):
                obstacle_positions = np.vstack((obstacle_positions,[0.65+np.cos(-angle2)*0.5*i/10, 3+np.sin(-angle2)*0.5*i/10]))
            for i in np.linspace(0,1,NUM_PATRICLES_PER_STOPPER):
                obstacle_positions = np.vstack((obstacle_positions,[i, 6]))
            obstacle_positions = obstacle_positions[1:]
            
            # loop throug all starting positions
            for version in [2]:
                if(not(angle1_deg==30 and angle2_deg == 45 and version==1) or (angle1_deg==30 and angle2_deg == 60 and version==2) or (angle1_deg==35 and angle2_deg == 50 and version==3) or (angle1_deg==40 and angle2_deg == 55 and version==1) or (angle1_deg==40 and angle2_deg == 45 and version==2) or (angle1_deg==45 and angle2_deg == 60 and version==3) or (angle1_deg==50 and angle2_deg == 50 and version==1) or (angle1_deg==55 and angle2_deg == 45 and version==2)  or (angle1_deg==60 and angle2_deg == 55 and version==3)):
                    filename = str(angle1_deg*5+30) + '_' + str(angle2_deg*5+45) + '_' + str(version)
                    print(filename)
                    with open(DATA_PATH+'/'+filename + '_9.npy', 'rb') as f:
                        datanpy = np.load(f)

                    data = trainModel.readData(datanpy, NUM_CARGO_PARTICLES)
                    k = EVERY_N #take every k-th position of dataset

                    # loop through all positions
                    for i in range(int((len(data))-7*k)):
                        train_data = np.vstack((np.hstack((data[[i],:],obstacle_positions[None])),np.hstack((data[[i+k],:],obstacle_positions[None])),np.hstack((data[[i+2*k],:],obstacle_positions[None])),np.hstack((data[[i+3*k],:],obstacle_positions[None])),np.hstack((data[[i+4*k],:],obstacle_positions[None])),np.hstack((data[[i+5*k],:],obstacle_positions[None]))))
                        train_examples = np.vstack((train_examples,train_data[None]))
                        train_labels = np.vstack((train_labels,np.hstack((data[[i+6*k],:],obstacle_positions[None]))))
    return train_examples, train_labels

if __name__ == "__main__":
    tf.disable_v2_behavior()
    main()
