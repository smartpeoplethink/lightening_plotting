
import numpy as np
import re
def removeFromListsBasedOnLastList(info, Excluded_type_number):
    adjusted_index = 0
    new_info = info.copy()
    for a in range(len(new_info[len(new_info)-1])):
        if new_info[len(new_info)-1][a-adjusted_index] in Excluded_type_number:
            
            for num in range(len(info)):
                new_info[num] = np.delete(new_info[num], a-adjusted_index)
            
            adjusted_index+=1
        
    return new_info
def Remove(numTest, Threshold, dir):
     if dir == "eql":
          if numTest == Threshold:
               return True
     if dir == "grtr":
          if numTest >= Threshold:
               return True
     if dir == "less":
          if numTest <= Threshold:
               return True
def removeFromListsBasedOnLastListAndExpression(info, Excluded_type_number, dir = "eql"):
    adjusted_index = 0
    new_info = info.copy()
    for a in range(len(new_info[len(new_info)-1])):
        
        if Remove(info[len(info)-1][a],Excluded_type_number, dir):
          for num in range(len(info)):
               new_info[num] = np.delete(new_info[num], a-adjusted_index)
            
          adjusted_index+=1
        
    return new_info
def removeBasedOnListAndExpression(info, limiter, Excluded_type_number, dir = "eql"):
    adjusted_index = 0
    new_info = info.copy()
    for a in range(len(limiter)):
        
        if Remove(limiter[a-adjusted_index],Excluded_type_number, dir):
          for num in range(len(info)):
               new_info[num] = np.delete(new_info[num], a-adjusted_index)
          limiter = np.delete(limiter, a-adjusted_index)
          adjusted_index+=1
        
    return new_info, limiter
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

def csvReader(name, locations, isint):
     if len(locations) != len(isint):
          return False
     lists = []
     for i in locations:
          
          lists.append(np.array([]))
     
     with open("info_storage/"+name+".csv") as inline:
          for line in inline:
              line_elements = line.split(",")
              for n in range(len(locations)):
                    element_index = locations[n]
                    info_of_index = line_elements[element_index]
                    if isint[n] == "int":
                        info_of_index = int(info_of_index)
                    if isint[n] == "flt":
                         info_of_index = float(info_of_index)
                    lists[n] = np.append(lists[n], info_of_index)
     return lists