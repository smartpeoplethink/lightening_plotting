import filereader
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature

Included = ["GC", "SL"]

Gradient_Pink = False
Spider_lightning_name = "Spider_GLM_50_8s_to_52_2s"

Excluded_type_number = []
file_names = ["50", "51", "52", "53", "54", "54", "55", "56", "57", "58", "59"]
#file_names = ["test"]
time = []
lat = []
long = []
Ltype = []
SLplotSize = 5
ICandGCplotSize = 5
basicName = ""
separator = " and "
for type in Included:
    basicName+=type
    basicName+=separator
basicName = basicName[:-len(separator)]
NonSLname = basicName[:]
if "SL" in basicName:
    NonSLname = basicName[:-(len(separator)+2)]
if Gradient_Pink:
    graphName = basicName+" using a gradient pink"
else:
    graphName = basicName
for i in range(len(file_names)):
    info = filereader.fileReader(file_names[i], [7, 9,10, 26], ["int", "flt","flt", "int"])

    if "GC" not in Included:
        info = filereader.removeFromListsBasedOnLastList(info, [0])
    if "IC" not in Included:
        info = filereader.removeFromListsBasedOnLastList(info, [1])
    

    time.extend([i+50]*len(info[0]))
    lat.extend(info[1])
    long.extend(info[2])
    Ltype.extend(info[3])
spider_lighning_info = filereader.csvReader(Spider_lightning_name, [8,9, 6,7], ["flt", "flt", "flt", "flt"])
latSL, longSL = spider_lighning_info[0], spider_lighning_info[1]

timeSL = spider_lighning_info[2]+spider_lighning_info[3]

#make it into a np array
time = np.array(time)
#Normalize

# timeSL-=min(timeSL)
# time -= 50
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
C = ax.scatter(long, lat, c = time, label=NonSLname, s=ICandGCplotSize)
if "SL" in Included and Gradient_Pink:
    pink_cmap = LinearSegmentedColormap.from_list("pink_gradient", ["pink", "deeppink", "mediumvioletred"])
    SL = ax.scatter(longSL, latSL, cmap = pink_cmap, c = timeSL, label="Spider Lightning", s=SLplotSize)
elif "SL" in Included:
    SL = ax.scatter(longSL, latSL, color = "pink", label="Spider Lightning", s=SLplotSize)

# Add legend and title
plt.legend()

plt.colorbar(C, label= "Time in minutes of "+ NonSLname+" (m)")
if "SL" in Included and Gradient_Pink:
    plt.colorbar(SL, label = "Time in seconds of SL (s)")
plt.title("Scatter Plot of "+graphName)

plt.savefig("./pictures/Version 1/"+graphName+".png")
plt.show()
