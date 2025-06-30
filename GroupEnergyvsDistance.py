
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import sorter
import pandas as pd
cmapGREEN = LinearSegmentedColormap.from_list("blue_gradient", ["purple", "blue", "lightblue", "green", "lightgreen"])
cmapORANGE = LinearSegmentedColormap.from_list("blue_gradient", ["purple", "blue", "lightblue", "green", "orange"])

cmap = cmapORANGE
TIME_FRAME = ["00:55:34.4","00:55:35.1"]
TIME_FRAMEO = ["00:57:50.8", "00:57:52.2"]
mainpoint = [-81.58, 26.23] # 55
mainpointO = [-81.58, 26.33] # 57


csv_file = r"C:\Users\Samuel Halperin\OneDrive\Documents\GitHub\lightening_plotting\info_storage\GLM_9_7_filtered2.csv"

dataSL = sorter.filter_and_sort_csv(csv_file, "hour", "minute", "second", "millisecond", TIME_FRAME[0], TIME_FRAME[1], ascending=True)

distance = ((dataSL["long"]- mainpoint[0])**2 + (dataSL["lat"]- mainpoint[1])**2)**(1/2)
current = dataSL["current"]


info= pd.DataFrame(
    {
        "Distance": distance,
        "Current": current
    }
)

info = info.sort_values(by = ["Distance"])


x = info["Distance"].to_list()
y = info["Current"].to_list()



SL = plt.scatter(x, y, label="Spider Lightning", c = "Cyan", s=10)

bin_width = 0.02
bins = np.arange(distance.min(), distance.max() + bin_width, bin_width)

# Assign bins
infoCut = pd.DataFrame({
    "x":[],
    "y":[]
})
index = 0
for bin in bins:
    
    maxY = 0
    while index<len(x) and x[index] <=bin:
        if y[index] > maxY:
            maxY = y[index]
            maxX = x[index]
        index+=1
        print("J")
    infoCut.loc[len(infoCut)] = [maxX, maxY]
    
print(infoCut["x"])
x = infoCut["x"].to_list()
y = infoCut["y"].to_list()


SL = plt.scatter(x, y, label="Spider Lightning", c = "Magenta", s=10)
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
plt.ylim(bottom=0)
plt.xlim(left=0)
plt.xlabel("Distance")
plt.ylabel("Group Energy")
plt.plot(x, p(x))
plt.show()
