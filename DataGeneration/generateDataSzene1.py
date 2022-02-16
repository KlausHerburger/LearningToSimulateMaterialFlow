"""Generates a dataset for a given configuration of Szene 1"""

import remote
import numpy as np
from scipy import io
import os
import time as timer

FILENAME = '20_3'

def time_diff_input(input_sequence):
    return input_sequence[1:, :] - input_sequence[:-1, :]

# Set virtuos filepath
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'VirtuosModels\\Szene1.epf')

# Set folders to save Matlab/Numpy file
m = (open("Data/Matlab/Szene1" + '/' + FILENAME + '.mat', 'wb'))
n = (open("Data/Numpy/Szene1" + '/' + FILENAME + '.npy', 'wb'))

# Start connection to virtuos, ramp up simulation and start update
virtousZugriff = remote.VirtuosZugriff()
virtousZugriff.virtuosDLL()
virtousZugriff.corbaInfo()
virtousZugriff.connectionCorba()
virtousZugriff.getProjectM(filename)
virtousZugriff.rampUpSim()
virtousZugriff.startUpdate()
virtousZugriff.startZyklUpdate()

# Get properties to read
valueIDgo = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[go]")
valueIDvel = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[vel]")
valueID1x = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[1x]")
valueID1y = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[1y]")
valueID2x = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[2x]")
valueID2y = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[2y]")
valueID3x = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[3x]")
valueID3y = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[3y]")
valueID4x = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[4x]")
valueID4y = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[4y]")
time = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[SimTime].[tsim]")
time_ = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[Time]")

# Start simulation
virtousZugriff.writeValue(valueIDgo[1], 1)

continueLoop = True
itr = 0
loopData = np.empty(shape=(1,9), dtype=np.float32)
prevTime = 0
start = timer.perf_counter()
"""Simulate one step while szene is not finished"""
while continueLoop:
    itr += 1
    virtousZugriff.simStep()
    time = virtousZugriff.readValue(time_)[1][1]

    # If simulation time is valid, read and save all positions
    if time != prevTime and time is not None:
        prevTime = time
        pos1x = virtousZugriff.readValue(valueID1x[1])[1][0]
        pos1y = virtousZugriff.readValue(valueID1y[1])[1][0]
        pos2x = virtousZugriff.readValue(valueID2x[1])[1][0]
        pos2y = virtousZugriff.readValue(valueID2y[1])[1][0]
        pos3x = virtousZugriff.readValue(valueID3x[1])[1][0]
        pos3y = virtousZugriff.readValue(valueID3y[1])[1][0]
        pos4x = virtousZugriff.readValue(valueID4x[1])[1][0]
        pos4y = virtousZugriff.readValue(valueID4y[1])[1][0]
        currentXData = [pos1x, pos2x, pos3x, pos4x]
        currentYData = [pos1y, pos2y, pos3y, pos4y]

        #Check if positions are valid
        assert not any(e < 0 or e > 1 for e in currentXData)
        assert not any(e < 0 or e > 3.2 for e in currentYData)
        assert not time < 0
        loopData = np.vstack((loopData,[pos1x, pos1y, pos2x, pos2y, pos3x, pos3y, pos4x, pos4y, time]))

        #Stop simulation if this condition is true
        if (itr > 3000) or ((pos1y > 3) or (pos2y > 3) or (pos3y > 3) or (pos4y > 3) ):
            stop = timer.perf_counter()
            print("Total time: " + str(stop - start))
            continueLoop = False

            # Linear interpolation of positions, if time difference varies
            velos = time_diff_input(loopData[1:])
            positions = loopData[1][None]
            for i in range(loopData[1:].shape[0]-2):
                factor = int(round(velos[i+1][8],2)/0.02)
                for j in range(factor):
                    pos = positions[-1, :] + velos[i+1]/factor
                    positions = np.vstack((positions, pos[None]))

            # Save positions as numpy array and matlab file
            np.save(n, positions)
            io.savemat(m, {'data': positions})

# Stop simulation
virtousZugriff.stopUpdate()
virtousZugriff.rampDownSim()
virtousZugriff.unloadDLL()


