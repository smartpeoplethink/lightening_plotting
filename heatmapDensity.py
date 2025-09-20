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
bin_quantity = 100
long_width = (area[1]-area[0])
lat_width = (area[3]-area[2])
quantity = np.array([[0]*bin_quantity]*bin_quantity)


fig, ax = plt.subplots()


# Loop over data dimensions and create text annotations.
for i in range(len(longSL)):
    distFromLeft = (longSL[i]-area[0])/long_width #scale from 0-1
    indexlong = int(distFromLeft*bin_quantity)
    distFromBottom = (latSL[i]-area[2])/lat_width #scale from 0-1
    indexlat = int((1-distFromBottom)*bin_quantity)
    
    quantity[indexlat][indexlong]+=1
    
areaLong = long_width/bin_quantity #0.008
areaLat = lat_width/bin_quantity
print(quantity)
data = quantity/(areaLat*areaLong)
# norm = plt.Normalize(0, 0.1)
# Apply Gaussian blur

data = gaussian_filter(data, sigma=3) 
im = ax.imshow(data, cmap = custom_cmap)
cbar = fig.colorbar(im, ax=ax)
ax.scatter(longSL, latSL, c = "white", s = 5)
im.set_extent(area)
plt.show()