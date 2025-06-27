SL_TIME_FRAME = ["00:55:34.4","00:55:35.1"]
SL_TIME_FRAMEO = ["00:57:50.8", "00:57:52.2"]

NLDN_TIME_FRAME = ["55:33.4", "55:36.1"]
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as patches
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
import ICandCGPandasHandler
import ICandGCHandler
import sorter
Camera = [-81.8, 26.37]
SL = True
Gradient_Pink = True
IC = True
GC = True
NonSLname = "DATA"

conditions = [
    ("solid pink SL", SL and not Gradient_Pink),
    ("gradient pink SL", SL and Gradient_Pink),
    ("GC", GC),
    ("IC", IC),
]

graphName = ", ".join([msg for msg, condition in conditions if condition])

longStart = -81.7
longEnd = -81.3
latStart = 26.1
latEnd = 26.5
locationMain = [-81.7, -81.3, 26.1, 26.5]
locationZoomOut = [-83, -80, 25, 28]
csv_file = r"C:\Users\Samuel Halperin\OneDrive\Documents\GitHub\lightening_plotting\info_storage\GLM_9_7_filtered2.csv"
# Start_Time = pd.to_datetime(Start_Time, format="%M:%S.%f")
# End_Time = pd.to_datetime(End_Time, format="%M:%S.%f")
dataSL = sorter.filter_and_sort_csv(csv_file, "hour", "minute", "second", "millisecond", SL_TIME_FRAME[0], SL_TIME_FRAME[1], ascending=True)
dataICandGC = ICandCGPandasHandler.load_and_filter_ualf_files(NLDN_TIME_FRAME, [0,1])

hSL = dataSL["hour"]
mSL = dataSL["minute"]
sSL = dataSL["second"]
msSL = dataSL["millisecond"]

timeSL = np.array(hSL*3600+60*mSL+(sSL+msSL/1000))

longSL = np.array(dataSL["long"])
latSL = np.array(dataSL["lat"])

# time -= 50
# plt.figure(figsize=(10, 5))
norm = plt.Normalize(50,59)
# #cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red", "orange", "yellow", "green","blue","indigo", "violet"])
# plt.scatter(long, lat, norm = norm,label = "IC & GC", c=time,s=10)

# plt.scatter(spider_lighnint_info[1], spider_lighnint_info[0], label = "Spider lightning", color = "pink", s = 1)



# Create a map with Cartopy
fig, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()}, figsize=(8, 6))

ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.LAKES)
ax.add_feature(cfeature.RIVERS)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=":")
ax.set_extent(locationZoomOut)

# Scatter different datasets with different colors

pink_cmap = LinearSegmentedColormap.from_list("pink_gradient", ["pink", "deeppink", "mediumvioletred"])
if not Gradient_Pink:
    pink_cmap = LinearSegmentedColormap.from_list("pink_gradient", ["deeppink", "deeppink"])
SL = ax.scatter(longSL, latSL, cmap = pink_cmap, c = timeSL, label="Spider Lightning", s=6)
# Add legend and title
C = ax.scatter(dataICandGC["Longitude"].to_list(), dataICandGC["Latitude"].to_list(), c = dataICandGC["TotalTimeMinutes"].to_list(), s=6)
ax.scatter(Camera[0], Camera[1], color = "black")
text = fig.text(0.5, 0.02, "Click a point to see intensity", ha='center', fontsize=12, color='black')


def on_click(event):
    if event.inaxes is not None:
        # Get click coordinates
        click_x, click_y = event.xdata, event.ydata
        distancesC = np.sqrt((long - click_x) ** 2 + (lat - click_y) ** 2)
        indexC = np.argmin(distancesC)  # Find closest point
        distancesS = np.sqrt((longSL - click_x) ** 2 + (latSL - click_y) ** 2)
        indexS = np.argmin(distancesS)  # Find closest point
        print("***********************************************************************************************")
        print(distancesS[indexS])
        # Set a threshold distance to avoid false clicks
        if distancesC[indexC] < 0.05 and distancesC[indexC]<=distancesS[indexS]:  
            text.set_text(f"Clicked on GC or IC ({long[indexC]:.2f}, {lat[indexC]:.2f}) with time {time[indexC]:.2f} and current {Current[indexC]:.2f}")  # Update text
            fig.canvas.draw_idle()
        elif distancesS[indexS]<0.05:
            text.set_text(f"Clicked on SL ({longSL[indexS]:.2f}, {latSL[indexS]:.2f})")  # Update text
            fig.canvas.draw_idle()
        else:
            text.set_text("Sorry, the click was not close enough")  # Update text
            fig.canvas.draw_idle()
# Connect click event to function
plt.gcf().canvas.mpl_connect('button_press_event', on_click)

gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5)
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': 12}
gl.ylabel_style = {'size': 12}


ax.add_patch(patches.Rectangle(
        xy=(longStart, latStart),  # point of origin.
        width=longEnd-longStart, height=latEnd-latStart, linewidth=1,
        color='red', fill=False))

plt.colorbar(C, label= "Time in minutes of "+ NonSLname+" (m)")
if SL and Gradient_Pink:
    plt.colorbar(SL, label = "Time in seconds of SL (s)")
plt.title("Scatter Plot of "+graphName)

plt.savefig("./pictures/Version 4/"+graphName+".png")
plt.show()
