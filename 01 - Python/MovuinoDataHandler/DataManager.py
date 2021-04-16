import threading
from threading import Thread
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time

class MovuinoDataSet(Thread):

    def __init__(self, filepath):

        self.filepath = filepath
        self.rawData = pd.read_csv(filepath + ".csv", sep=",")

        self.time = []

        # liste de vecteurs numpy
        self.acceleration = []
        self.gyroscope = []
        self.magnetometer = []

        self.normAcceleration = []
        self.normGyroscope = []
        self.normMagnetometer = []

        self.velocity = [np.array([0, 0, 0])]
        self.pos = [np.array([0, 0, 0])]
        self.posAng = [np.array([0, 0, 0])]

        self.time = list(self.rawData["time"])

        self.nb_line = len(self.time)

        self.compteur_line = 0
        self.thread = Thread.__init__(self)

    def run(self):
        for k in range(self.nb_line):
            self.acceleration.append(np.array([self.rawData["ax"][k], self.rawData["ay"][k], self.rawData["az"][k]]))
            self.gyroscope.append(np.array([self.rawData["gx"][k], self.rawData["gy"][k], self.rawData["gz"][k]]))
            self.magnetometer.append(np.array([self.rawData["mx"][k], self.rawData["my"][k], self.rawData["mz"][k]]))

            self.normAcceleration.append(np.linalg.norm(self.acceleration[k]))
            self.normGyroscope.append(np.linalg.norm(self.gyroscope[k]))


            if k > 1:

                self.posAng.append(np.array([self.TrapezeIntegration(self.gyroscope[k-1][0], self.gyroscope[k][0], self.time[k-1], self.time[k]),
                                             self.TrapezeIntegration(self.gyroscope[k-1][1], self.gyroscope[k][1], self.time[k-1],self.time[k]),
                                             self.TrapezeIntegration(self.gyroscope[k-1][2], self.gyroscope[k][2], self.time[k-1],self.time[k])]))

            if k == self.nb_line-1 :
                self.ConvertArray()
                self.StockIntoNewFile()

    def ConvertArray(self):
        self.acceleration = np.array(self.acceleration)
        self.gyroscope = np.array(self.gyroscope)
        self.magnetometer = np.array(self.magnetometer)

        print(self.posAng)
        self.posAng = np.array(self.posAng)
        self.pos = np.array(self.pos)

        self.rawData["normAccel"] = self.normAcceleration
        self.rawData["normGyr"] = self.normGyroscope

    def StockIntoNewFile(self):
        self.rawData.to_csv(self.filepath + "_treated" + ".csv", sep=",", index=False, index_label=False)
        """"
        plt.figure()
        plt.plot(self.time, self.normAcceleration)
        plt.plot(self.time, self.acceleration[:, 0])
        plt.plot(self.time, self.acceleration[:, 1])
        plt.plot(self.time, self.acceleration[:, 2])
        plt.show()
        """
        plt.figure()
        plt.plot(self.time, self.posAng[:, 0])
        plt.plot(self.time, self.gyroscope[:, 1])
        plt.show()

    def TrapezeIntegration(self, y1, y2, t1, t2, dt=0):
        return np.trapz([y1, y2], [t1, t2])


