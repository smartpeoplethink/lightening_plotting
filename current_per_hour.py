#ihhyi
import matplotlib.pyplot as plt
import datetime
import numpy as np
import re

value = np.array([])
time = np.array([])
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
              
              value = np.append(value, float(info[13])) #TEST
              time = np.append(time, float(info[5])*60*60+float(info[6])*60+float(info[7]))
x = time
y = value

plt.plot(x,y)
plt.show()