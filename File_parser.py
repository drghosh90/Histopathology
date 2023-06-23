import os 

file=[]
ouput="Histopathology\Dataset\Final Dataset\T-19-22 adeno CA"
for i in os.listdir("Histopathology/Dataset/Renamed Data/T-19-22 ductal CA"):
    print(i)

# for i in range(0,len(file)):
#     if(i%3 !=0):
#         t.append(file[i])
#         print(file[i])
# print(t)