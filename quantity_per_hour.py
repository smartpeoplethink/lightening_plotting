import matplotlib.pyplot as plt
import datetime
import numpy as np
import re
currentHour = 0
quantityHourly = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
hours = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])
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
                #print(info)
                # print(type(info[9]))
            time = int(info[5])
            quantityHourly[time]+=1

x = hours
y = quantityHourly

plt.plot(x,y)
plt.show()