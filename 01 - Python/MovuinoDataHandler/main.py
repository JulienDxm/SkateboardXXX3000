import serial
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from integratinoFunctions import *
from DisplayFunctions import Display
from mvtAnalyseFunctions import OnGround
import DataManager as dm
import os


folderPath = "..\\..\\Data\\SessionMuette_16_04_2021\\"
fileName = "record_1"
fullDataPath = folderPath + fileName


toDataManage = True
toExtract = False

thrd_list = []

# --------- Data Extraction from Movuino ----------
if toExtract:

    isReading = False
    ExtractionCompleted = False
    arduino = serial.Serial('COM9', baudrate=115200, timeout=1.)
    line_byte = ''
    line_str = ''
    datafile = []
    nbRecord = 1

    while ExtractionCompleted != True :

        line_byte = arduino.readline()
        line_str = line_byte.decode("utf-8")

        if ("XXX_end" in line_str and isReading == True):
            isReading = False
            ExtractionCompleted = True
            print("End of data sheet")

            with open(fullDataPath + "_" + str(nbRecord) + ".csv", "w") as file:
                file.writelines(datafile)
            if toDataManage:
                thrd_list.append(dm.MovuinoDataSet(fullDataPath + "_" + str(nbRecord)))
                thrd_list[-1].start()

        if ("NEW RECORD" in line_str and isReading == True):

            print("NEW RECORD : " + str(nbRecord))

            with open(fullDataPath + "_" + str(nbRecord) + ".csv", "w") as file:
                file.writelines(datafile)
            datafile = []
            line_str = ''

            if toDataManage:
                thrd_list.append(dm.MovuinoDataSet(fullDataPath + "_" + str(nbRecord)))
                thrd_list[-1].start()
            nbRecord += 1


        if (isReading):
            if line_str != '':
                datafile.append(line_str[:-1])
                print("Add Data")

        if ("XXX_beginning" in line_str):
            isReading = True


if toDataManage and not toExtract:
    thrd = dm.MovuinoDataSet(fullDataPath)
    thrd.start()
"""
#Data MAnage
if toDataManage:

    rawData = pd.read_csv(fullDataPath + ".csv", sep=",")

    time = []

    # liste de vecteurs numpy
    acceleration = []
    gyroscope = []
    magnetometer = []

    normAcceleration = []
    normGyroscope = []
    normMagnetometer = []

    velocity = [np.array([[0], [0], [0]])]
    pos = [np.array([[0], [0], [0]])]
    posAng = [np.array([[0], [0], [0]])]

    time = list(rawData["time"])
    for k in range(len(rawData["ax"])):
        acceleration.append(np.array([rawData["ax"][k], rawData["ay"][k], rawData["az"][k]]))
        gyroscope.append(np.array([rawData["gx"][k], rawData["gy"][k], rawData["gz"][k]]))
        magnetometer.append(np.array([rawData["mx"][k], rawData["my"][k], rawData["mz"][k]]))

        normAcceleration.append(np.linalg.norm(acceleration[k]))
        normGyroscope.append(np.linalg.norm(gyroscope[k]))

    for i in range(3):
        velocity[i] = Euler(time, acceleration[i], velocity[i][0])
        pos[i] = Euler(time, velocity[i], pos[i][0])
        posAng[i] = Euler(time, gyroscope[i], posAng[i][0])

    normAcceleration = EuclidienNormListVector(acceleration)
    normGyroscope = EuclidienNormListVector(gyroscope)
    normMagnetometer = EuclidienNormListVector(magnetometer)

    Display("a,v,pos", time, acceleration, velocity, pos)
    Display("omega, theta", time, gyroscope, posAng)
    Display("Magnetometer", time, magnetometer)

    print(acceleration)
    acceleration = np.array(acceleration)
    print(acceleration[:,0])
    #Display("a", time, acceleration[:,0])


    rawData["posAngX"] = posAng[0]
    rawData["posAngY"] = posAng[1]
    rawData["posAngZ"] = posAng[2]
    rawData["VelocityX"] = velocity[0]
    rawData["VelocityY"] = velocity[1]
    rawData["VelocityZ"] = velocity[2]
    rawData["posX"] = pos[0]
    rawData["posY"] = pos[1]
    rawData["posZ"] = pos[2]

    rawData["normAccel"] = normAcceleration
    rawData["normGyr"] = normGyroscope
    plt.figure()
    plt.plot(time, normAcceleration)
    plt.plot(time, acceleration[:,0])
    plt.plot(time, acceleration[:,1])
    plt.plot(time, acceleration[:,2])
    plt.show()


    rawData.to_csv(fullDataPath + "_treated" + ".csv", sep=",", index=False, index_label=False)
"""