import filereader
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature

Included = ["GC", "SL"]

Gradient_Pink = True
Spider_lightning_name = "GLM_9_7_filtered2"

Excluded_type_number = []
file_names = ["55", "56", "57","58"]
StartSeconds = 0
EndSeconds = 20
# file_names = ["57_20-58_03"]
time = []
lat = []
long = []
Ltype = []
Current = []
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
    info = filereader.fileReader(file_names[i], [6,7, 9,10, 26, 19], ["int","int", "flt","flt", "int", "flt"])

    if "GC" not in Included:
        info = filereader.removeFromListsBasedOnLastList(info, [0])
    if "IC" not in Included:
        info = filereader.removeFromListsBasedOnLastList(info, [1])
    if i == 0:
        [info[0], info[2], info[3], info[4], info[5], info[1]] = filereader.removeFromListsBasedOnLastListAndExpression([info[0], info[2], info[3], info[4], info[5], info[1]], StartSeconds, "less")
    if i == len(file_names)-1:
        [info[0], info[2], info[3], info[4], info[5], info[1]] = filereader.removeFromListsBasedOnLastListAndExpression([info[0], info[2], info[3], info[4], info[5], info[1]], EndSeconds, "grtr")
    
    for i in range(len(info[0])):
        info[0][i]+=info[1][i]/60
    
    
    
    time.extend(info[0])
    lat.extend(info[2])
    long.extend(info[3])
    Ltype.extend(info[4])
    Current.extend(info[5])
spider_lighning_info = filereader.csvReader(Spider_lightning_name, [8,9, 6,7], ["flt", "flt", "flt", "flt"])
latSL, longSL = spider_lighning_info[0], spider_lighning_info[1]

timeSL = spider_lighning_info[2]+spider_lighning_info[3]

#make it into a np array
time = np.array(time)
#Normalize

# timeSL-=min(timeSL)
# time -= 50
# plt.figure(figsize=(10, 5))
norm = plt.Normalize(50,59)
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
C = ax.scatter(long, lat, c = time, label=NonSLname, norm = norm , s=ICandGCplotSize)
if "SL" in Included and Gradient_Pink:
    pink_cmap = LinearSegmentedColormap.from_list("pink_gradient", ["pink", "deeppink", "mediumvioletred"])
    SL = ax.scatter(longSL, latSL, cmap = pink_cmap, c = timeSL, label="Spider Lightning", s=SLplotSize)
elif "SL" in Included:
    SL = ax.scatter(longSL, latSL, color = "pink", label="Spider Lightning", s=SLplotSize)
C = ax.scatter(long, lat, c = time, label=NonSLname, norm = norm , s=ICandGCplotSize)
# Add legend and title
text = fig.text(0.5, 0.02, "Click a point to see intensity", ha='center', fontsize=12, color='black')


def on_click(event):
    if event.inaxes is not None:
        # Get click coordinates
        click_x, click_y = event.xdata, event.ydata
        distances = np.sqrt((long - click_x) ** 2 + (lat - click_y) ** 2)
        index = np.argmin(distances)  # Find closest point

        # Set a threshold distance to avoid false clicks
        if distances[index] < 0.05:  
            text.set_text(f"Clicked on point ({long[index]:.2f}, {lat[index]:.2f}) with time {time[index]:.2f} and current {Current[index]:.2f}")  # Update text
            fig.canvas.draw_idle() 

# Connect click event to function
plt.gcf().canvas.mpl_connect('button_press_event', on_click)



plt.legend()

plt.colorbar(C, label= "Time in minutes of "+ NonSLname+" (m)")
if "SL" in Included and Gradient_Pink:
    plt.colorbar(SL, label = "Time in seconds of SL (s)")
plt.title("Scatter Plot of "+graphName)

plt.savefig("./pictures/Version 1/"+graphName+".png")
plt.show()
