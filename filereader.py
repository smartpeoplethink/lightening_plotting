
import numpy as np
import re

def fileReader(name, locations):
     lists = []
     for i in locations:
          
          lists.append(np.array([]))
     
     with open("info_storage/"+name+".txt") as inline:
          for line in inline:
              line = re.sub(r'\s+', ' ', line)
              currentColumn = 0
              currentIndex = 0
              currentdata = ""
              while currentColumn < len(line):
                     if line[currentColumn]==" ":
                        #print(currentIndex)
                        if currentIndex in locations:
                         #   print(currentdata)
                            lists[locations.index(currentIndex)] = np.append(lists[locations.index(currentIndex)], currentdata)
                          #  print(lists[locations.index(currentIndex)])
                        currentdata = ""
                        currentColumn+=1
                        currentIndex+=1 
                     else: 
                            currentdata+=line[currentColumn]
                            currentColumn+=1
     return lists