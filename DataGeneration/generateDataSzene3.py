import remote
import numpy as np
from scipy import io
import os

FILENAME = "Gen_51_39_63_71_3_9"

def time_diff_input(input_sequence):
    return input_sequence[1:, :] - input_sequence[:-1, :]

# Set virtuos filepath
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'VirtuosModels\\Szene3.epf')

# Set folders to save Matlab/Numpy file
m = (open("Data/Matlab/Szene3/GeneralisationSets" + '/' + FILENAME + '.mat', 'wb'))
n = (open("Data/Numpy/Szene3/GeneralisationSets" + '/' + FILENAME + '.npy', 'wb'))

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
valueID5x = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[5x]")
valueID5y = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[5y]")
valueID6x = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[6x]")
valueID6y = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[6y]")
valueID7x = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[7x]")
valueID7y = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[7y]")
valueID8x = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[8x]")
valueID8y = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[8y]")
valueID9x = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[9x]")
valueID9y = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[9y]")
time = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[SimTime].[tsim]")
time_ = virtousZugriff.readValueID("[Main].[Mikro_physicbased].[Time]")

# Start simulation
virtousZugriff.writeValue(valueIDgo[1], 1)

continueLoop = True
itr = 0
loopData = np.empty(shape=(1,19), dtype=np.float32)
prevTime = 0
"""Simulate one step while szene is not finished"""
while continueLoop:
    itr += 1
    virtousZugriff.simStep()
    time = virtousZugriff.readValue(time_)[1][1]

    # Ff simulation time is valid, read and save all positions
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
        pos5x = virtousZugriff.readValue(valueID5x[1])[1][0]
        pos5y = virtousZugriff.readValue(valueID5y[1])[1][0]
        pos6x = virtousZugriff.readValue(valueID6x[1])[1][0]
        pos6y = virtousZugriff.readValue(valueID6y[1])[1][0]
        pos7x = virtousZugriff.readValue(valueID7x[1])[1][0]
        pos7y = virtousZugriff.readValue(valueID7y[1])[1][0]
        pos8x = virtousZugriff.readValue(valueID8x[1])[1][0]
        pos8y = virtousZugriff.readValue(valueID8y[1])[1][0]
        pos9x = virtousZugriff.readValue(valueID9x[1])[1][0]
        pos9y = virtousZugriff.readValue(valueID9y[1])[1][0]
        currentXData = [pos1x,pos2x,pos3x,pos4x,pos5x,pos6x,pos7x,pos8x,pos9x]
        currentYData = [pos1y,pos2y,pos3y,pos4y,pos5y,pos6y,pos7y,pos8y,pos9y]

        # Check if positions are valid
        assert not any(e < 0 or e > 1 for e in currentXData)
        assert not any(e < 0 or e > 6 for e in currentYData)
        assert not time<0
        loopData = np.vstack((loopData, [pos1x,pos1y,pos2x,pos2y,pos3x,pos3y,pos4x,pos4y,pos5x,pos5y,pos6x,pos6y,pos7x,pos7y,pos8x,pos8y,pos9x,pos9y,time]))

        # Stop simulation if this condition is true
        if (itr > 5000) or ((pos1y > 5.5) and (pos2y > 5.5) and (pos3y > 5.5) and (pos4y > 5.5) and (pos5y > 5.5) and (pos6y > 5.5) and (pos7y > 5.5) and (pos8y > 5.5) and (pos9y > 5.5) ):
            continueLoop = False

            # Linear interpolation of positions, if time difference varies
            velos = time_diff_input(loopData[1:])
            positions = loopData[1][None]
            for i in range(loopData[1:].shape[0]-4):
                i = i+2
                factor = int(round(velos[i+1][18],2)/0.02)
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


