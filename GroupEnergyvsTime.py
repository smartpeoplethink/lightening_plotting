
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import numpy as np
import sorter
from GroupEnergyvsDensityEachPlottedSeperately import groupenergy

TIME_FRAME = ["00:55:34.4","00:55:35.1"]
TIME_FRAMEOO = ["00:57:50.8", "00:57:52.2"]
TIME_FRAMEO = ["00:00:00.0", "02:00:00.0"]


csv_file = r"/home/samuel-halperin/Documents/Programming/lightening_plotting/info_storage/GLM_9_7_filtered2.csv"

dataSL = sorter.filter_and_sort_csv(csv_file, "hour", "minute", "second", "millisecond", TIME_FRAME[0], TIME_FRAME[1], ascending=True)

longSL = np.array(dataSL["long"])
latSL = np.array(dataSL["lat"])
energy = np.array(dataSL["groupenergy"])
time = np.array(dataSL["second"]+dataSL["millisecond"]/1000)


SL = plt.scatter(time, energy, c = time, label="Spider Lightning", s=1)
# Add legend and title
text = plt.text(0.5, 0.02, "", ha='center', fontsize=12, color='black')

plt.colorbar(SL, label = "The time of the lighting strikes")
plt.show()
print("Finished")