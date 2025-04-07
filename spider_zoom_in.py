
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import sorter


TIME_FRAME = ["00:55:34.4","00:55:35.1"]
TIME_FRAMEO = ["00:57:50.8", "00:57:52.2"]


csv_file = r"C:\Users\Samuel Halperin\OneDrive\Documents\GitHub\lightening_plotting\info_storage\GLM_9_7_filtered2.csv"

dataSL = sorter.filter_and_sort_csv(csv_file, "hour", "minute", "second", "millisecond", TIME_FRAME[0], TIME_FRAME[1], ascending=True)

longSL = np.array(dataSL["long"])
latSL = np.array(dataSL["lat"])
time = np.array(dataSL["second"]+dataSL["millisecond"]/1000)

# Create a map with Cartopy
fig, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()}, figsize=(8, 6))

# Add coastlines and features
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=":")
ax.set_extent([-82, -81, 26.068, 26.6])
cmap = LinearSegmentedColormap.from_list("blue_gradient", ["purple", "blue", "lightblue", "green", "lightgreen"])
SL = ax.scatter(longSL, latSL, cmap = cmap, c = time, label="Spider Lightning", s=5)
# Add legend and title
text = fig.text(0.5, 0.02, "Click a point to see intensity", ha='center', fontsize=12, color='black')


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



plt.legend()
plt.colorbar(SL, label = "The time of the lighting strikes")
plt.savefig("./pictures/Version 3/spider_zoom_in_57.png")
plt.show()
