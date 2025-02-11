import filereader
from matplotlib import animation
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import re
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pprint

Excluded_type_number = []
file_names = ["50", "51", "52", "53", "54", "54", "55", "56", "57", "58", "59"]
#file_names = ["test"]
time = []
lat = []
long = []
Ltype = []
pink_cmap = LinearSegmentedColormap.from_list("pink_gradient", ["white", "pink", "deeppink"])


for i in range(len(file_names)):
    info = filereader.fileReader(file_names[i], [7, 9,10, 26], ["int", "flt","flt", "int"])


    info = filereader.removeFromListsBasedOnLastList(info, [1])

    time.extend([i+50]*len(info[0]))
    lat.extend(info[1])
    long.extend(info[2])
    Ltype.extend(info[3])
spider_lighning_info = filereader.csvReader("GLM_9_7_filtered2", [4,5,6,8,9], ["flt", "flt", "flt", "flt", "flt"])
latSL, longSL = spider_lighning_info[3], spider_lighning_info[4]

timeSL = spider_lighning_info[0]*60+spider_lighning_info[1]+spider_lighning_info[2]/60

#make it into a np array
time = np.array(time)
#Normalize

timeSL-=min(timeSL)
time -= 50
# plt.figure(figsize=(10, 5))
# norm = plt.Normalize(50,59)
# #cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red", "orange", "yellow", "green","blue","indigo", "violet"])
# plt.scatter(long, lat, norm = norm,label = "IC & GC", c=time,s=10)

# plt.scatter(spider_lighnint_info[1], spider_lighnint_info[0], label = "Spider lightning", color = "pink", s = 1)



# Create a map with Cartopy
fig, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()}, figsize=(8, 6))

# Add coastlines and features
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=":")
ax.set_extent([-82, -81, 25, 26.6])

# Scatter different datasets with different colors
SL = ax.scatter(longSL, latSL, color = "pink", label="Spider Lightning", s=1)
C = ax.scatter(long, lat, c = time, label="GC", s=5)

# Add legend and title
plt.legend()
plt.colorbar(C, label= "Time in minutes of GC")
#plt.colorbar(SL, label = "Time in minutes of SL")
plt.title("Scatter Plot of Multiple Data Sets on a Map")

plt.show()