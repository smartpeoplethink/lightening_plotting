# light blue - yellow - red
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import sorter
from scipy.ndimage import gaussian_filter



TIME_FRAME = ["00:55:34.4","00:55:35.1"]
TIME_FRAMEO = ["00:57:50.8", "00:57:52.2"]


csv_file = r"C:\Users\Samuel Halperin\OneDrive\Documents\GitHub\lightening_plotting\info_storage\GLM_9_7_filtered2.csv"

dataSL = sorter.filter_and_sort_csv(csv_file, "hour", "minute", "second", "millisecond", TIME_FRAME[0], TIME_FRAME[1], ascending=True)

longSL = np.array(dataSL["long"])
latSL = np.array(dataSL["lat"])
current = np.array(dataSL["current"])

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
    
    bins[indexlat][indexlong]+=current[i]*10**15
    quantity[indexlat][indexlong]+=1



# Avoid divide-by-zero
result = np.zeros_like(bins, dtype=float)
mask = quantity != 0
result[mask] = bins[mask] / quantity[mask]
areaLong = long_width/bin_quantity #0.008
areaLat = lat_width/bin_quantity

GroupEnergy = result.ravel()
Density = quantity.ravel()/ (areaLat*areaLong)
# Apply Gaussian blur
ax.scatter(Density, GroupEnergy)

ax.set_xlabel("Density (occurences per degrees squared)")
ax.set_ylabel("Group Energy (joules)")
fig.tight_layout()
plt.show()