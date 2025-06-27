#55:34.4--55:35.1
#57:50.8--57:52.2

import SpiderLightningHandler
import filereader
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
def ICandGC(Included):
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
    for i in range(10):
        minute = str(50+i)
        info = filereader.fileReader(minute, [6,7, 9,10, 19, 26], ["int","int", "flt","flt", "flt", "int"])
        if "GC" not in Included:
            info = filereader.removeFromListsBasedOnLastList(info, [0])
        if "IC" not in Included:
            info = filereader.removeFromListsBasedOnLastList(info, [1])
        
        for i in range(len(info[0])):
            info[0][i]+=info[1][i]/60
        
        
        
        time.extend(info[0])
        lat.extend(info[2])
        long.extend(info[3])
        Current.extend(info[4])
        Ltype.extend(info[5])
    return time, lat, long, Ltype, Current
