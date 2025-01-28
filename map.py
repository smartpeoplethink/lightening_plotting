from matplotlib import animation
import matplotlib.pyplot as plt
import numpy as np
import re
import cartopy.crs as ccrs
import cartopy.feature as cfeature

fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.PlateCarree()})


# Data for plotting
latitude = np.array([])
longitude = np.array([])
value = np.array([])
with open("info_storage/info.txt") as inline:
       for line in inline:
              line = re.sub(r'\s+', ' ', line)
              info = []
              index = 0
              currentdata = ""
              while index < len(line):
                     if line[index]==" ":
                            index+=1
                            info.append(str(currentdata))
                            currentdata = ""
                     else:
                            currentdata+=line[index]
                            index+=1
              print(info)
              # print(type(info[9]))
              latitude = np.append(latitude, float(info[9]))
              longitude = np.append(longitude, float(info[10]))
              value = np.append(value, float(info[13]))
# Plot the data
scatter = ax.scatter(longitude, latitude, c=value, cmap='plasma', s=10)
plt.colorbar(scatter, label='Current')

# Add map features
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.STATES, linestyle=':')

# Set extent to focus on the southeastern US
ax.set_extent([-105, -75, 15, 31])
ax.set_title('Lightning Strikes on January 1, 2018')
# Add gridlines and labels
gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5)
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': 12}
gl.ylabel_style = {'size': 12}


plt.savefig('plot.png', format='png')
plt.show()