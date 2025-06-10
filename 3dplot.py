import matplotlib.pyplot as plt
import numpy as np

# Fixing random state for reproducibility

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

longSL = np.array(dataSL["long"])
latSL = np.array(dataSL["lat"])
time = np.array(dataSL["second"]+dataSL["millisecond"]/1000)
energy = np.array(dataSL["current"])
# Create a map with Cartopy
# fig, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()}, figsize=(8, 6))

# # Add coastlines and features
# ax.add_feature(cfeature.COASTLINE)
# ax.add_feature(cfeature.BORDERS, linestyle=":")
# ax.set_extent([-82, -81, 26.068, 26.6])
# SL = ax.scatter(longSL, latSL, energy, cmap = cmap, c = time, label="Spider Lightning", s=5)
# # Add legend and title
# text = fig.text(0.5, 0.02, "Click a point to see intensity", ha='center', fontsize=12, color='black')







fig = plt.figure()
ax = fig.add_subplot(projection='3d')

sc = ax.scatter(longSL, latSL, energy, cmap= cmap, c = time)
fig.colorbar(sc, ax=ax, label='Time (s)')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Group Energy (J)')

plt.show()