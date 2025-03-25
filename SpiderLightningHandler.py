#55:34.4--55:35.1
#57:50.8--57:52.2

import filereader
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
def SpiderLightning(Kept_Values, Kept_DataTypes, Start_minute, End_minute, Start_second, End_second,
                     Spider_lightning_name = "GLM_9_7_filtered2", Gradient_Pink = True):
    if Gradient_Pink:
        graphName = "Graph of SL using a gradient pink"
    else:
        graphName = "Graph of SL"
    spider_lighning_info = filereader.csvReader(Spider_lightning_name, Kept_DataTypes, Kept_Values)
    mins = spider_lighning_info[0]
    shortened_info = spider_lighning_info
    shortened_info.pop(0)
    shortened_info, mins = filereader.removeBasedOnListAndExpression(shortened_info, mins, Start_minute, dir = "less")
    
    shortened_info, mins = filereader.removeBasedOnListAndExpression(shortened_info, mins,  End_minute, dir = "grtr")
    

    shortened_info.insert(0, mins)
    return graphName, shortened_info

