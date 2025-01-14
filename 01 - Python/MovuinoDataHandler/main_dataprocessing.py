import dataSet.SkateboardXXX3000DataSet as sk
import tools.FilterMethods as fm
import tools.integratinoFunctions as ef
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

############   SETTINGS   #############

device = 'skateboardXXX3000'  # devices available : skateboardXXX3000 / sensitivePen / globalDataSet

folderPath = "..\\..\\06 - Data\\tricks_come\\"
filename = "record"  # generic name numbers will be added for duplicates

filter = 5

# -------- Data processing ----------------------

print("Processing : " + folderPath + filename)
skateDataSet = sk.SkateboardXXX3000DataSet(folderPath + filename, filter)
Te = skateDataSet.Te

print("sample frequency : " + str(1 / Te))
# Filtering
skateDataSet.acceleration_lp = fm.MeanFilter(skateDataSet.acceleration, filter)
skateDataSet.gyroscope_lp = fm.MeanFilter(skateDataSet.gyroscope, filter)
skateDataSet.magnetometer_lp = fm.MeanFilter(skateDataSet.magnetometer, filter)

# Integration of values :
skateDataSet.velocity = ef.EulerIntegration(skateDataSet.acceleration, Te)
skateDataSet.ThetaGyr = ef.EulerIntegration(skateDataSet.gyroscope, Te)
skateDataSet.pos = ef.EulerIntegration(skateDataSet.velocity, Te)

# Stock in processed.csv
skateDataSet.stockProcessedData(folderPath + filename[:-4] + "_treated.csv")


