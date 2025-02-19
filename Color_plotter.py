import filereader
from matplotlib import animation   
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np
import re
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pprint
Excluded_type_number = []
file_names = ["50", "51", "52", "53", "54", "54", "55", "56", "57", "58", "59"]
#file_names = ["test"]
timeIC = []
latIC = []
longIC = []
LtypeIC = []
timeGC = []
latGC = []
longGC = []
LtypeGC = []


for i in range(len(file_names)):
    info = filereader.fileReader(file_names[i], [7, 9,10, 26], ["int", "flt","flt", "int"])
    infoGC = filereader.removeFromListsBasedOnLastList(info, [1])
    

    timeGC.extend([i+50]*len(infoGC[0]))
    latGC.extend(infoGC[1])
    longGC.extend(infoGC[2])
    LtypeGC.extend(infoGC[3])

    infoIC = filereader.removeFromListsBasedOnLastList(info, [0])
    
    timeIC.extend([i+50]*len(infoIC[0]))
    latIC.extend(infoIC[1])
    longIC.extend(infoIC[2])
    LtypeIC.extend(infoIC[3])
spider_lighnint_info = filereader.csvReader("GLM_9_7_filtered2", [8,9], ["flt", "flt"])
plt.figure(figsize=(10, 5))

plt.scatter(longIC,latIC, label = "IC", color = "blue", s = 5)

plt.scatter(longGC, latGC, label = "GC", color = "red", s = 5)

plt.scatter(spider_lighnint_info[1], spider_lighnint_info[0], label = "Spider_lightning", color = "pink", s = 5)

# Customize the plot
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Multiple Data Sets on One Graph")
plt.legend()  # Show legend
plt.grid(True)  # Add grid

plt.savefig('plot.png', format='png')
plt.show()