TIME_FRAME = ["00:55:34.4","00:55:35.1"]
TIME_FRAMEO = ["00:57:50.8", "00:57:52.2"]
#IC = green; CG = Blue
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import ICandGCHandler
import sorter

SL = True
Gradient_Pink = True
IC = True
GC = False
NonSLname = "DATA"

conditions = [
    ("solid pink SL", SL and not Gradient_Pink),
    ("gradient pink SL", SL and Gradient_Pink),
    ("GC", GC),
    ("IC", IC),
]

graphName = "Lightning graph with minute around " + ", ".join([msg for msg, condition in conditions if condition])



csv_file = r"C:\Users\Samuel Halperin\OneDrive\Documents\GitHub\lightening_plotting\info_storage\GLM_9_7_filtered2.csv"

dataSL = sorter.filter_and_sort_csv(csv_file, "hour", "minute", "second", "millisecond", TIME_FRAME[0], TIME_FRAME[1], ascending=True)
incl = []
if GC:
    incl.append("GC")
if IC:
    incl.append("IC")
print(incl)
minutes = ["50", "51", "52", "53", "54", "55", "56", "57", "58", "59"]
minutes = ["55", "56"]
dataICandGC = ICandGCHandler.ICandGC(incl, 
                                     minutes,
                                       3, 5)
time, lat, long, Ltype, Current = dataICandGC

hSL = dataSL["hour"]
mSL = dataSL["minute"]
sSL = dataSL["second"]
msSL = dataSL["millisecond"]

timeSL = np.array(hSL*3600+60*mSL+(sSL+msSL/1000))

longSL = np.array(dataSL["long"])
latSL = np.array(dataSL["lat"])

# time -= 50
# plt.figure(figsize=(10, 5))
norm = plt.Normalize(50,59)
# #cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red", "orange", "yellow", "green","blue","indigo", "violet"])
# plt.scatter(long, lat, norm = norm,label = "IC & GC", c=time,s=10)

# plt.scatter(spider_lighnint_info[1], spider_lighnint_info[0], label = "Spider lightning", color = "pink", s = 1)



# Create a map with Cartopy
fig, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()}, figsize=(8, 6))

# Add coastlines and features
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=":")
ax.set_extent([-82, -81, 25, 26.6])

# Scatter different datasets with different colors
C = ax.scatter(long, lat, c = time, norm = norm , s=5)
pink_cmap = LinearSegmentedColormap.from_list("pink_gradient", ["pink", "deeppink", "mediumvioletred"])
if not Gradient_Pink:
    pink_cmap = LinearSegmentedColormap.from_list("pink_gradient", ["deeppink", "deeppink"])
SL = ax.scatter(longSL, latSL, cmap = pink_cmap, c = timeSL, label="Spider Lightning", s=5)
# Add legend and title
text = fig.text(0.5, 0.02, "Click a point to see intensity", ha='center', fontsize=12, color='black')


def on_click(event):
    if event.inaxes is not None:
        # Get click coordinates
        click_x, click_y = event.xdata, event.ydata
        distancesC = np.sqrt((long - click_x) ** 2 + (lat - click_y) ** 2)
        indexC = np.argmin(distancesC)  # Find closest point
        distancesS = np.sqrt((longSL - click_x) ** 2 + (latSL - click_y) ** 2)
        indexS = np.argmin(distancesS)  # Find closest point
        print("***********************************************************************************************")
        print(distancesS[indexS])
        # Set a threshold distance to avoid false clicks
        if distancesC[indexC] < 0.05 and distancesC[indexC]<=distancesS[indexS]:  
            text.set_text(f"Clicked on GC or IC ({long[indexC]:.2f}, {lat[indexC]:.2f}) with time {time[indexC]:.2f} and current {Current[indexC]:.2f}")  # Update text
            fig.canvas.draw_idle()
        elif distancesS[indexS]<0.05:
            text.set_text(f"Clicked on SL ({longSL[indexS]:.2f}, {latSL[indexS]:.2f})")  # Update text
            fig.canvas.draw_idle()
        else:
            text.set_text("Sorry, the click was not close enough")  # Update text
            fig.canvas.draw_idle()
# Connect click event to function
plt.gcf().canvas.mpl_connect('button_press_event', on_click)



plt.legend()

plt.colorbar(C, label= "Time in minutes of "+ NonSLname+" (m)")
if SL and Gradient_Pink:
    plt.colorbar(SL, label = "Time in seconds of SL (s)")
plt.title("Scatter Plot of "+graphName)

plt.savefig("./pictures/Version 4/"+graphName+".png")
plt.show()
