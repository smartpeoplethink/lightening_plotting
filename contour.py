import matplotlib.pyplot as plt
import numpy as np
import sorter

TIME_FRAMEO = ["00:55:34.4","00:55:35.1"]
TIME_FRAME = ["00:57:50.8", "00:57:52.2"]


csv_file = r"C:\Users\Samuel Halperin\OneDrive\Documents\GitHub\lightening_plotting\info_storage\GLM_9_7_filtered2.csv"

dataSL = sorter.filter_and_sort_csv(csv_file, "hour", "minute", "second", "millisecond", TIME_FRAME[0], TIME_FRAME[1], ascending=True)


plt.style.use('_mpl-gallery-nogrid')

long = dataSL["long"].to_list() 
lat = dataSL["lat"].to_list()
X, Y = long, lat
Z = dataSL["current"].to_list()
levels = np.linspace(min(Z), max(Z), 7)

# plot
fig, ax = plt.subplots()

ax.tricontourf(X, Y, Z)

plt.show()
