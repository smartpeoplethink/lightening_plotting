SL_TIME_FRAMEO = ["00:55:34.4","00:55:35.1"]
SL_TIME_FRAME = ["00:57:50.8", "00:57:52.2"]

NLDN_TIME_FRAME = ["55:33.4", "55:36.1"]
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
import ICandCGPandasHandler
import ICandGCHandler
import sorter

SL = True
Gradient_Pink = False
IC = False
GC = False
NonSLname = "DATA"

conditions = [
    ("solid pink SL", SL and not Gradient_Pink),
    ("gradient pink SL", SL and Gradient_Pink),
    ("GC", GC),
    ("IC", IC),
]

graphName = "Lightning graph"



csv_file = r"C:\Users\Samuel Halperin\OneDrive\Documents\GitHub\lightening_plotting\info_storage\GLM_9_7_filtered2.csv"

dataSL = sorter.filter_and_sort_csv(csv_file, "hour", "minute", "second", "millisecond", SL_TIME_FRAME[0], SL_TIME_FRAME[1], ascending=True)

dataICandGC = ICandCGPandasHandler.load_and_filter_ualf_files(NLDN_TIME_FRAME, [0,1])


hSL = dataSL["hour"]
mSL = dataSL["minute"]
sSL = dataSL["second"]
msSL = dataSL["millisecond"]

timeSL = np.array(hSL*60+mSL+(sSL+msSL/1000)/60)

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

# Add coastlines and features

ax.add_feature(cfeature.BORDERS, linestyle=":")
ax.set_extent([-81.7, -81.3, 26.1, 26.5])

# Scatter different datasets with different colors

C = ax.scatter(dataICandGC["Longitude"].to_list(), dataICandGC["Latitude"].to_list(), c = dataICandGC["TotalTimeMinutes"].to_list(), s=6)
pink_cmap = LinearSegmentedColormap.from_list("pink_gradient", ["pink", "deeppink", "mediumvioletred"])
if not Gradient_Pink:
    pink_cmap = LinearSegmentedColormap.from_list("pink_gradient", ["deeppink", "deeppink"])
SL = ax.scatter(longSL, latSL, cmap = pink_cmap, c = timeSL, label="Spider Lightning", s=6)
# Add legend and title
text = fig.text(0.5, 0.02, "Click a point to see intensity", ha='center', fontsize=12, color='black')


def on_click(event):
    if event.inaxes is not None:
        # Get click coordinates
        click_x, click_y = event.xdata, event.ydata
        distancesC = np.sqrt((dataICandGC["Longitude"].to_list() - click_x) ** 2 + (dataICandGC["Latitude"].to_list() - click_y) ** 2)
        indexC = np.argmin(distancesC)  # Find closest point
        distancesS = np.sqrt((longSL - click_x) ** 2 + (latSL - click_y) ** 2)
        indexS = np.argmin(distancesS)  # Find closest point
        print("***********************************************************************************************")
        print(distancesS[indexS])
        # Set a threshold distance to avoid false clicks
        if distancesC[indexC] < 0.05 and distancesC[indexC]<=distancesS[indexS]:  
            
            text.set_text(
                f"Clicked on NLDN ({dataICandGC['Longitude'].to_list()[indexC]:.2f}, "
                f"{dataICandGC['Latitude'].to_list()[indexC]:.2f}) "
                f"with time {dataICandGC.loc[indexC, 'TimeStr']} "
                f"and current {dataICandGC['Current'].to_list()[indexC]:.2f}"
            )
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



def format_minutes_seconds(x, pos):
    mins = int(x)
    secs = int(round((x - mins) * 60))
    return f'{mins}:{secs:02d}'

# Add colorbar with formatter
cbar = plt.colorbar(C, label= "Time in minutes of "+ NonSLname+" (m)")
cbar.set_label("Time (MM:SS)")
cbar.ax.yaxis.set_major_formatter(FuncFormatter(format_minutes_seconds))


if SL and Gradient_Pink:
    cbar = plt.colorbar(SL, label = "Time in seconds of SL (s)")
    cbar.set_label("Time (MM:SS)")
    cbar.ax.yaxis.set_major_formatter(FuncFormatter(format_minutes_seconds))

plt.title("Scatter Plot of "+graphName)

plt.savefig("./pictures/Version 4/"+graphName+".png")
plt.show()