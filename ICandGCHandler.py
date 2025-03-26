#55:34.4--55:35.1
#57:50.8--57:52.2

import SpiderLightningHandler
import filereader
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
def ICandGC(Included, file_names, StartSeconds, EndSeconds):
    time = []
    lat = []
    long = []
    Ltype = []
    Current = []
    basicName = ""
    separator = " and "
    for type in Included:
        basicName+=type
        basicName+=separator
    basicName = basicName[:-len(separator)]
    for i in range(len(file_names)):
        info = filereader.fileReader(file_names[i], [6,7, 9,10, 19, 26], ["int","int", "flt","flt", "flt", "int"])
        if "GC" not in Included:
            info = filereader.removeFromListsBasedOnLastList(info, [0])
        if "IC" not in Included:
            info = filereader.removeFromListsBasedOnLastList(info, [1])
        if i == 0:
            [info[0], info[2], info[3], info[4], info[5], info[1]] = filereader.removeFromListsBasedOnLastListAndExpression([info[0], info[2], info[3], info[4], info[5], info[1]], StartSeconds, "less")
        if i == len(file_names)-1:
            [info[0], info[2], info[3], info[4], info[5], info[1]] = filereader.removeFromListsBasedOnLastListAndExpression([info[0], info[2], info[3], info[4], info[5], info[1]], EndSeconds, "grtr")
        
        for i in range(len(info[0])):
            info[0][i]+=info[1][i]/60
        
        
        
        time.extend(info[0])
        lat.extend(info[2])
        long.extend(info[3])
        Current.extend(info[4])
        Ltype.extend(info[5])
    return time, lat, long, Ltype, Current
