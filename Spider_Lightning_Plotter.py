import filereader
from matplotlib import animation
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np
import re
import cartopy.crs as ccrs
import cartopy.feature as cfeature

fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.PlateCarree()})
info = filereader.fileReader("54", [7,9,10], ["int","flt","flt"]) 
second = info[0]
latitude = info[1]
longitude = info[2]
norm = plt.Normalize(0,60)
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red", "orange", "yellow", "green","blue","indigo", "violet"])
scatter = ax.scatter(longitude, latitude, c=second, cmap=cmap,norm = norm, s=10)
plt.colorbar(scatter, label='Time is seconds')

# Add map features
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.STATES, linestyle=':')

# Set extent to focus on the southeastern US
ax.set_extent([-82, -81, 25, 26.6])
ax.set_title('Lightning Strikes on January 1, 2018')
# Add gridlines and labels
# print(latitude[2])
gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5)
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': 12}
gl.ylabel_style = {'size': 12}


plt.savefig('plot.png', format='png')
plt.show()