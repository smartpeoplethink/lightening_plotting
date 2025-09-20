
from matplotlib import patches
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyArrowPatch
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import sorter
cmapGREEN = LinearSegmentedColormap.from_list("blue_gradient", ["purple", "blue", "lightblue", "green", "lightgreen"])
cmapORANGE = LinearSegmentedColormap.from_list("blue_gradient", ["purple", "blue", "lightblue", "green", "orange"])

cmap = cmapORANGE

TimeFrame55 = True

TIME_FRAME55 = ["00:55:34.4","00:55:35.1"]
TIME_FRAME57 = ["00:57:50.8", "00:57:52.2"]
TIME_FRAME = TIME_FRAME55 if TimeFrame55 else TIME_FRAME57

PATCHESLONGS57 = [-81.5622, -81.4898,-81.5674 ,-81.5726, -81.6449]
PATCHESLATS57 = [26.203, 26.3525,26.2781 ,26.3531,26.2035]
PATCHESENDLONG57 = [-81.5621, -81.4896, -81.5673 ,-81.5724, -81.6448]
PATCHESENDLAT57 = [26.2032, 26.3527,26.2783 , 26.3533 ,26.2037]

PATCHESLONGS55 = [-81.5635, -81.6175, -81.5875, -81.5793, -81.54]
PATCHESLATS55 = [26.2039, 26.1985, 26.225, 26.4292, 26.13]
PATCHESENDLONG55 = [-81.5631, -81.6025,-81.57,-81.5791, -81.51]
PATCHESENDLAT55 = [26.2042, 26.2075, 26.245, 26.4293, 26.18]



PATCHESLONGS = PATCHESLONGS55 if TimeFrame55 else PATCHESLONGS57
PATCHESLATS = PATCHESLATS55 if TimeFrame55 else PATCHESLATS57
PATCHESENDLONG = PATCHESENDLONG55 if TimeFrame55 else PATCHESENDLONG57
PATCHESENDLAT = PATCHESENDLAT55 if TimeFrame55 else PATCHESENDLAT57




COLORS = ["Black", "deepskyblue", "chartreuse", "aqua", "gold"]
csv_file = r"C:\Users\Samuel Halperin\OneDrive\Documents\GitHub\lightening_plotting\info_storage\GLM_9_7_filtered2.csv"

dataSL = sorter.filter_and_sort_csv(csv_file, "hour", "minute", "second", "millisecond", TIME_FRAME[0], TIME_FRAME[1], ascending=True)
dataSL["time"] = dataSL["second"]+dataSL["millisecond"]/1000

dataSL = dataSL.sort_values(by = ["time"]).reset_index(drop=True)

longSL = np.array(dataSL["long"])
latSL = np.array(dataSL["lat"])
time = np.array(dataSL["second"]+dataSL["millisecond"]/1000)
current = np.array(dataSL["current"])

# Create a map with Cartopy
fig, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()}, figsize=(8, 6))

# Add coastlines and features
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=":")
ax.set_extent([-81.7, -81.3, 26.1, 26.5])

SL = ax.scatter(longSL, latSL, cmap = cmap, c = time, label="Spider Lightning", s=5)
for i in range(len(dataSL) - 1):
    lon1, lat1 = dataSL["long"].iloc[i], dataSL["lat"].iloc[i]
    lon2, lat2 = dataSL["long"].iloc[i + 1], dataSL["lat"].iloc[i + 1]
    
    dist_squared = (lon2 - lon1) ** 2 + (lat2 - lat1) ** 2
    if dist_squared < 0.025 ** 2:
        arrow = FancyArrowPatch(
            (lon1, lat1), (lon2, lat2),
            transform=ccrs.PlateCarree(),
            arrowstyle='-|>',
            color='red',
            linewidth=1,
            mutation_scale=10,
            clip_on=True  # <-- This ensures it won't spill outside the axes
        )
        ax.add_patch(arrow)






# Add legend and title
text = fig.text(0.5, 0.02, "", ha='center', fontsize=12, color='black')


def on_click(event):
    if event.inaxes is not None:
        # Get click coordinates
        click_x, click_y = event.xdata, event.ydata
        distancesS = np.sqrt((longSL - click_x) ** 2 + (latSL - click_y) ** 2)
        indexS = np.argmin(distancesS)  # Find closest point
        if distancesS[indexS]<0.05:
            TIME = (time[indexS])
            print(TIME)
            text.set_text(f"Clicked on SL ({longSL[indexS]:.2f}, {latSL[indexS]:.2f}) with and time in seconds of {TIME:.2f}")  # Update text
            fig.canvas.draw_idle()
        else:
            text.set_text("Sorry, the click was not close enough")  # Update text
            fig.canvas.draw_idle()
        print(time[indexS])
# Connect click event to function
plt.gcf().canvas.mpl_connect('button_press_event', on_click)






gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5)

gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': 12}
gl.ylabel_style = {'size': 12}





# REctangles

for i in range(5):
    x = PATCHESLONGS[i]
    y = PATCHESLATS[i]
    width = PATCHESENDLONG[i] - PATCHESLONGS[i]
    height = PATCHESENDLAT[i] - PATCHESLATS[i]
    
    if (width+height)/2 > 0.001:
        # ax.add_patch(patches.Rectangle(
        #     xy=(x, y),  # point of origin.
        #     width=width, height=height, linewidth=5,
        #     color=COLORS[i], fill=False))
        pass
    else:
        ax.plot(x+width/2,y+height/2, marker='o', color = COLORS[i], markersize = 6)



plt.colorbar(SL, label = "The time of the lighting strikes")
plt.savefig("./pictures/Version 3/spider_zoom_in_57.png")
plt.show()
