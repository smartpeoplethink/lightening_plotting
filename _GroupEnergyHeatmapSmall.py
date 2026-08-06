# light blue - yellow - red
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import sorter
from scipy.ndimage import gaussian_filter
# from matplotlib.ticker import FuncFormatter
# from matplotlib.ticker import MultipleLocator
import matplotlib.ticker as ticker
from pathlib import Path

# Define the custom colormap
custom_cmap = LinearSegmentedColormap.from_list(
    'lightblue_yellow_red',
    ['blue', 'green', 'yellow', 'orange', 'red']
)

TIME_FRAME = ["00:55:34.4","00:55:35.1"]
TIME_FRAMEO = ["00:57:50.8", "00:57:52.2"]

home_dir = r"//"
csv_file = home_dir+r"info_storage/GLM_9_7_filtered2.csv"

dataSL = sorter.filter_and_sort_csv(csv_file, "hour", "minute", "second", "millisecond", TIME_FRAME[0], TIME_FRAME[1], ascending=True)

longSL = np.array(dataSL["long"])
latSL = np.array(dataSL["lat"])
current = np.array(dataSL["groupenergy"])

area = [-81.7, -81.3, 26.1, 26.5]
bin_width = 100 #was 20
long_width = (area[1]-area[0])
lat_width = (area[3]-area[2])
bins = np.array([[0]*bin_width]*bin_width)
quantity = np.array([[-1]*bin_width]*bin_width)


fig, ax = plt.subplots()


# Loop over data dimensions and create text annotations.
for i in range(len(longSL)):
    if (area[0] < longSL[i] < area[1] and area[2] < latSL[i] < area[3]):
        distFromLeft = (longSL[i]-area[0])/long_width #scale from 0-1
        indexlong = int(distFromLeft*bin_width)
        distFromBottom = (latSL[i]-area[2])/lat_width #scale from 0-1
        indexlat = int((1-distFromBottom)*bin_width)
        bins[indexlat][indexlong]+=current[i]*10**15
        if (quantity[indexlat][indexlong] == -1):
            quantity[indexlat][indexlong] = 1
        else:
            quantity[indexlat][indexlong]+=1
    
data = bins / quantity

# Apply Gaussian blur
data = gaussian_filter(data, sigma=3)

im = ax.imshow(data, cmap=custom_cmap)

cbar = fig.colorbar(im, ax=ax)
cbar.ax.set_title(r'$\times10^{-15}$', pad=8)
cbar.set_label("Group Energy (J)")

ax.scatter(longSL, latSL, c = "white", s = 5)



# Every 0.1°
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.05))
ax.xaxis.set_major_formatter(
    ticker.FuncFormatter(lambda x, pos: f"{abs(x):.1f}")
)
ax.yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda y, pos: f"{y:.2f}")
)


im.set_extent(area)
fig.tight_layout()
plt.show()


save_dir = Path(home_dir+"Pictures/Version 20")
name = "groupenergyheatmap"

i = 1
while (save_dir / f"{name}_{i}.png").exists():
    i += 1

fig.savefig(save_dir / f"{name}_{i}.png", dpi=300, bbox_inches="tight")