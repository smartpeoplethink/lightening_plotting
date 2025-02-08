import filereader
from matplotlib import animation
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np
import re
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pprint

file_names = ["50", "51", "52", "53", "54", "54", "55", "56", "57", "58", "59"]
#file_names = ["test"]
truncate_seconds = True
time = []
latitude = []
longitude = []
Ltype = []
Excluded = []
for i in range(len(file_names)):
    info = filereader.fileReader(file_names[i], [7, 9,10, 26], ["int", "flt","flt", "int"])
    #print(info)
    info = filereader.removeFromListsBasedOnLastList(info, Excluded)       
    print(info) 
    if truncate_seconds:
        current_time = [i+50]*len(info[0])
        
    else:
        current_time = [i+50]*len(info[0])+info[0]/60
    time.extend(current_time)
    latitude.extend(info[1])
    longitude.extend(info[2])
    Ltype.extend(info[3])

#color_set = ["red", "orange", "yellow", "green","blue", "indigo", "violet", "pink", "black", ]
fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.PlateCarree()})

norm = plt.Normalize(50,59)
#cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red", "orange", "yellow", "green","blue","indigo", "violet"])
scatter = ax.scatter(longitude, latitude, norm = norm, c=time,s=10)
plt.colorbar(scatter, label='Time in minutes')

# Add map features
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.STATES, linestyle=':')


# Set extent to focus on the southeastern US
ax.set_extent([-82, -81, 25, 26.6])
ax.set_title('Lightning Strikes')
# Add gridlines and labels
# print(latitude[2])
gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5)
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': 12}
gl.ylabel_style = {'size': 12}


plt.savefig('plot.png', format='png')
plt.show()