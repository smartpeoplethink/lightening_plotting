# light blue - yellow - red
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import sorter
from scipy.ndimage import gaussian_filter

# Define the custom colormap
custom_cmap = LinearSegmentedColormap.from_list(
    'lightblue_yellow_red',
    ['blue', 'green', 'yellow', 'orange', 'red']
)

TIME_FRAMEO = ["00:55:34.4","00:55:35.1"]
TIME_FRAME = ["00:57:50.8", "00:57:52.2"]


csv_file = r"C:\Users\Samuel Halperin\OneDrive\Documents\GitHub\lightening_plotting\info_storage\GLM_9_7_filtered2.csv"

dataSL = sorter.filter_and_sort_csv(csv_file, "hour", "minute", "second", "millisecond", TIME_FRAME[0], TIME_FRAME[1], ascending=True)

longSL = np.array(dataSL["long"])
latSL = np.array(dataSL["lat"])
current = np.array(dataSL["current"])

area = [-81.7, -81.3, 26.1, 26.5]
bin_width = 20
long_width = (area[1]-area[0])
lat_width = (area[3]-area[2])
bins = np.array([[0]*bin_width]*bin_width)
quantity = np.array([[-1]*bin_width]*bin_width)


fig, ax = plt.subplots()


# Loop over data dimensions and create text annotations.
for i in range(len(longSL)):
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
im = ax.imshow(data, cmap = custom_cmap)
cbar = fig.colorbar(im, ax=ax)
cbar.set_label("Group Energy 10^-15 Joules")
ax.scatter(longSL, latSL, c = "pink", s = 5)
im.set_extent(area)
fig.tight_layout()
plt.show()