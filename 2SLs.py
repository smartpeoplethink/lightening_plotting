SL_TIME_FRAME55 = ["00:55:34.4","00:55:35.1"]
SL_TIME_FRAME57 = ["00:57:50.8", "00:57:52.2"]

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


NonSLname = "DATA"



graphName = "Lightning graph"



csv_file = r"C:\Users\Samuel Halperin\OneDrive\Documents\GitHub\lightening_plotting\info_storage\GLM_9_7_filtered2.csv"

dataSL55 = sorter.filter_and_sort_csv(csv_file, "hour", "minute", "second", "millisecond", SL_TIME_FRAME55[0], SL_TIME_FRAME55[1], ascending=True)
dataSL57 = sorter.filter_and_sort_csv(csv_file, "hour", "minute", "second", "millisecond", SL_TIME_FRAME57[0], SL_TIME_FRAME57[1], ascending=True)


longSL55 = np.array(dataSL55["long"])
latSL55 = np.array(dataSL55["lat"])

longSL57 = np.array(dataSL57["long"])
latSL57 = np.array(dataSL57["lat"])
# Create a map with Cartopy
fig, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()}, figsize=(8, 6))

# Add coastlines and features

ax.add_feature(cfeature.BORDERS, linestyle=":")
ax.set_extent([-81.7, -81.3, 26.1, 26.5])

# Scatter different datasets with different colors

# SL = ax.scatter(longSL55, latSL55, color = "Red", label="Spider Lightning", s=6)

SL = ax.scatter(longSL57, latSL57, color = "Blue", label="Spider Lightning", s=6)

# Remove all spines
for spine in ax.spines.values():
    spine.set_visible(False)


gl = ax.gridlines(draw_labels=False, linestyle='', alpha=0)
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': 12}
gl.ylabel_style = {'size': 12}

gl.grid = False
gl.Axes = False
gl.Title = False
gl.Outline = False

plt.title("")

plt.savefig("./pictures/Version 18/Blue57.png", transparent = True)
plt.show()