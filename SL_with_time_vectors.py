
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import sorter
cmapGREEN = LinearSegmentedColormap.from_list("blue_gradient", ["purple", "blue", "lightblue", "green", "lightgreen"])
cmapORANGE = LinearSegmentedColormap.from_list("blue_gradient", ["purple", "blue", "lightblue", "green", "orange"])

cmap = cmapORANGE
TIME_FRAMEO = ["00:55:34.4","00:55:35.1"]
TIME_FRAME = ["00:57:50.8", "00:57:52.2"]


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

SL = ax.scatter(longSL, latSL, cmap = cmap, c = current, label="Spider Lightning", s=5)
for i in range(len(dataSL) - 1):
    lon1, lat1 = dataSL["long"].iloc[i], dataSL["lat"].iloc[i]
    lon2, lat2 = dataSL["long"].iloc[i + 1], dataSL["lat"].iloc[i + 1]
    
    dist_squared = (lon2 - lon1) ** 2 + (lat2 - lat1) ** 2
    if dist_squared < 0.025 ** 2:
        ax.annotate(
            '', xy=(lon2, lat2), xytext=(lon1, lat1),
            arrowprops=dict(arrowstyle="->", color="red", lw=1),
            transform=ccrs.PlateCarree()
        )
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

plt.colorbar(SL, label = "The time of the lighting strikes")
plt.savefig("./pictures/Version 3/spider_zoom_in_57.png")
plt.show()
