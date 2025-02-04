
import numpy as np
import re

def fileReader(name, locations, isint):
     if len(locations) != len(isint):
          return False
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
                        if currentIndex in locations and currentdata!="":
                              
                              typeIndex = locations.index(currentIndex)
                              if (isint[typeIndex] == "int"):
                                   currentdata = int(currentdata)
                                   
                              if (isint[typeIndex] == "flt"):
                                   currentdata = float(currentdata)

                              
                              lists[typeIndex] = np.append(lists[typeIndex], currentdata)
                              
                          #  print(lists[locations.index(currentIndex)])
                        currentdata = ""
                        currentColumn+=1
                        currentIndex+=1 
                     else: 
                            currentdata+=line[currentColumn]
                            currentColumn+=1
     return lists