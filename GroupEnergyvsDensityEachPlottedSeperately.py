# light blue - yellow - red
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import sorter
from scipy.ndimage import gaussian_filter

def calcDensityByIndex(x, dens):
    row = x // bin_quantity
    col = x % bin_quantity
    return dens[row][col]

TIME_FRAMEo = ["00:55:34.4","00:55:35.1"]
TIME_FRAME = ["00:57:50.8", "00:57:52.2"]



csv_file = r"/home/samuel-halperin/Documents/Programming/lightening_plotting/info_storage/GLM_9_7_filtered2.csv"

dataSL = sorter.filter_and_sort_csv(csv_file, "hour", "minute", "second", "millisecond", TIME_FRAME[0], TIME_FRAME[1], ascending=True)

longSL = np.array(dataSL["long"])
latSL = np.array(dataSL["lat"])
time = np.array(dataSL["second"]+dataSL["millisecond"]/1000)

# Create a map with Cartopy
fig, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()}, figsize=(8, 6))

# Add coastlines and features
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=":")
ax.set_extent([-81.7, -81.3, 26.1, 26.5])

SL = ax.scatter(longSL, latSL, c = time, label="Spider Lightning", s=5)
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
# plt.savefig("./pictures/Version 3/spider_zoom_in_57.png")
plt.show()

dataSL = sorter.filter_and_sort_csv(csv_file, "hour", "minute", "second", "millisecond", TIME_FRAME[0], TIME_FRAME[1], ascending=True)

longSL = np.array(dataSL["long"])
latSL = np.array(dataSL["lat"])
groupenergy = np.array(dataSL["groupenergy"])
binIndex = []
binDensity = np.zeros(len(longSL))


area = [-81.7, -81.3, 26.1, 26.5]
bin_quantity = 50
long_width = (area[1]-area[0])
lat_width = (area[3]-area[2])
bins = np.array([[0]*bin_quantity]*bin_quantity)
quantity = np.array([[0]*bin_quantity]*bin_quantity)


fig, ax = plt.subplots()
ax.set_title("Bin amount per side: "+ str(bin_quantity)+"; Time: "+TIME_FRAME[0])

# Loop over data dimensions and create text annotations.
for i in range(len(longSL)):
    distFromLeft = (longSL[i]-area[0])/long_width #scale from 0-1
    indexlong = int(distFromLeft*bin_quantity)
    distFromBottom = (latSL[i]-area[2])/lat_width #scale from 0-1
    indexlat = int((1-distFromBottom)*bin_quantity)
    
    bins[indexlat][indexlong]+=groupenergy[i]*10**15
    quantity[indexlat][indexlong]+=1
    binIndex.append(indexlat*bin_quantity+indexlong)



# Avoid divide-by-zero
result = np.zeros_like(bins, dtype=float)
mask = quantity != 0
result[mask] = bins[mask] / quantity[mask]
areaLong = long_width/bin_quantity #0.008
areaLat = lat_width/bin_quantity

BinGroupEnergy = result.ravel()
Density = quantity.ravel()/ (areaLat*areaLong)

for i in range(len(longSL)):
    binDensity[i] = calcDensityByIndex(binIndex[i], quantity)
    #print(binDensity[i], groupenergy[i-1], longSL[i], latSL[i])
    
#print(np.min(binIndex))

ax.scatter(binDensity, groupenergy)
##ax.scatter(Density, BinGroupEnergy)

ax.set_xlabel("Density (occurences per degrees squared)")
ax.set_ylabel("Group Energy (joules)")
fig.tight_layout()
plt.show()