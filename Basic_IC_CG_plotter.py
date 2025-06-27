import ICandCGPandasHandler

NLDN_TIME_FRAME = ["50:33.4", "55:36.1"]
#IC = green; CG = Blue
import matplotlib.pyplot as plt

data = ICandCGPandasHandler.load_and_filter_ualf_files(NLDN_TIME_FRAME)
print(f"Data shape: {data.shape}")
print(data.head())



plt.scatter(data["Longitude"].to_list(), data["Latitude"].to_list())


plt.show()

print("Latitude range:", data['Latitude'].min(), "to", data['Latitude'].max())
print("Longitude range:", data['Longitude'].min(), "to", data['Longitude'].max())