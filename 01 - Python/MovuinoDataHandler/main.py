import serial
import DataManager as dm
import DisplayFunctions as disp
import OnlyExtract as extractMovDat
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def butter_bandpass(lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs #sampling frequency
        low = lowcut / nyq
        high = highcut / nyq
        sos = signal.butter(order, [low, high], analog=False, btype='band', output='sos')
        return sos

def butter_bandpass_filter(sig, lowcut, highcut, fs, order=5):
        sos = butter_bandpass(lowcut, highcut, fs, order=order)
        sig_filtered = signal.sosfilt(sos, sig)
        return sig_filtered

folderPath = "..\\..\\Data\\Cri_tricks_stationary_5_goodOne\\Only_tricks_notransition\\"
#folderPath = "..\\..\\Data\\Movuino-heel_50HZ_smooth15\\"
fileName = "record"

path = folderPath + fileName

serialPort = 'COM9'

toDataManage = True
toExtract = False

nb_files = 0
nbRecord = 0

# --------- Data Extraction from Movuino ----------
if toExtract:

    isReading = False
    ExtractionCompleted = False
    arduino = serial.Serial(serialPort, baudrate=115200, timeout=1.)
    line_byte = ''
    line_str = ''
    datafile = []
    nbRecord = 1

    while ExtractionCompleted != True:
        line_byte = arduino.readline()
        line_str = line_byte.decode("utf-8")

        if "XXX_end" in line_str and isReading == True :
            isReading = False
            ExtractionCompleted = True
            print("End of data sheet")

            with open(path + "_" + str(nbRecord) + ".csv", "w") as file:
                file.writelines(datafile)

        if "NEW RECORD" in line_str and isReading == True :
            with open(path + "_" + str(nbRecord) + ".csv", "w") as file:
                file.writelines(datafile)

            datafile = []
            line_str = ''
            nbRecord += 1

        if (isReading):
            if line_str != '':
                datafile.append(line_str[:-1])
                print("Add Data")

        if ("XXX_beginning" in line_str):
            isReading = True


if toDataManage:
    print(nbRecord)
    nbRecord = 11
    for i in range(1, nbRecord+1):
        dataSet = dm.MovuinoDataSet(folderPath + fileName + "_"+str(i))
        dataSet.run()
        Te = dataSet.Te
        print(1/Te)
    """

    a_pb = butter_bandpass_filter(dataSet.acceleration[:, 2], 0.15, 4.5, 1/Te, order = 3)
    a_pb_butter = dm.BandPassButterworthFilter(4, [0.3, 0.9], dataSet.acceleration[:, 2])

    ax_pb = dm.LowPassFilter(dataSet.time, dataSet.acceleration[:, 2], dataSet.time[-1] / len(dataSet.time), fc=0.001)
    ax_pb_2 = dm.LowPassButterworthFilter(3, 0.3, dataSet.acceleration[:, 2])

    plt.plot(dataSet.time, dataSet.acceleration[:, 2], color='silver', label='Signal')
    plt.plot(dataSet.time, a_pb, color='#cc0000', label='Signal filtré passe bande')
    plt.plot(dataSet.time, a_pb_butter, color='blue', label='Signal filtré passe bande')
    plt.grid(True, which='both')
    plt.legend(loc="best")
    plt.title("Filtre passe-bas du 1er ordre")
    plt.show()

    plt.plot(dataSet.time, dataSet.acceleration[:, 2], color='silver', label='Signal')
    plt.plot(dataSet.time, ax_pb, color='#cc0000', label='Signal filtré passe bande')
    plt.plot(dataSet.time, ax_pb_2, color='blue', label='Signal filtré passe bande')
    plt.grid(True, which='both')
    plt.legend(loc="best")
    plt.title("Filtre passe-bas du 1er ordre")
    plt.show()

    for i in range(nbRecord):
        dataSet = dm.MovuinoDataSet(path + "_" + str(i+1))
        dataSet.run()
    """
    """
        ax_pb = dm.LowPassFilter(dataSet.time, dataSet.acceleration[:,0], dataSet.time[-1]/len(dataSet.time), fc = 0.05)
        ax_pb_2 = dm.LowPassButterworthFilter(3, 0.09, dataSet.acceleration[:,0])


        g_pb = []
        g_pb_butter = []
        g = [dataSet.gyroscope[:,0],dataSet.gyroscope[:,1],dataSet.gyroscope[:,2]]
        g_pb.append(dm.LowPassFilter(dataSet.time, dataSet.gyroscope[:,0], dataSet.time[-1]/len(dataSet.time), fc = 1))
        g_pb_butter.append(dm.LowPassButterworthFilter(5, 0.9, dataSet.gyroscope[:,0]))
        g_pb.append(dm.LowPassFilter(dataSet.time, dataSet.gyroscope[:,1], dataSet.time[-1]/len(dataSet.time), fc = 1))
        g_pb_butter.append(dm.LowPassButterworthFilter(5, 0.9, dataSet.gyroscope[:,1]))
        g_pb.append(dm.LowPassFilter(dataSet.time, dataSet.gyroscope[:,2], dataSet.time[-1]/len(dataSet.time), fc = 1))
        g_pb_butter.append(dm.LowPassButterworthFilter(5, 0.9, dataSet.gyroscope[:,2]))

        disp.Display("Gyroscope filtré", dataSet.time, g, g_pb, g_pb_butter)

        a_pb = []
        a_pb_butter = []
        a = [dataSet.acceleration[:, 0], dataSet.acceleration[:, 1], dataSet.acceleration[:, 2]]
        a_pb_butter.append(dm.BandPassButterworthFilter(4, [0.1, 0.3], dataSet.acceleration[:, 0]))
        a_pb_butter.append(dm.BandPassButterworthFilter(4, [0.1, 0.3], dataSet.acceleration[:, 1]))
        a_pb_butter.append(dm.BandPassButterworthFilter(4, [0.1, 0.15], dataSet.acceleration[:, 2]))
        disp.Display("Acceleration", dataSet.time, a, a_pb_butter)
        #disp.Display("Gyroscope filtré", dataSet.time, g, g_pb, g_pb_butter)
        
        plt.plot(dataSet.time, dataSet.acceleration[:,0], color='silver', label='Signal')
        plt.plot(dataSet.time, ax_pb, color='#cc0000', label='Signal filtré lowpass')
        plt.plot(dataSet.time, ax_pb_2, color='black', label='Signal filtré filtfilt')
        plt.grid(True, which='both')
        plt.legend(loc="best")
        plt.title("Filtre passe-bas du 1er ordre")
        plt.show()
        """

