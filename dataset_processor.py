"""
import os,shutil
folder = "E:/Histopathology/Dataset/Raw Data/T-25-22 adeno CA"
files = os.listdir(folder)
f_count = 1
zoom = ["40x","100x","400x"]
z_id = 0
for f in files:
    shutil.copyfile(f"{folder}/{f}", "%s/%03d-%s.tif"%("E:/Histopathology/Dataset/Renamed Data/T-25-22 adeno CA",f_count,zoom[z_id]))
    z_id += 1
    if z_id == 3:
        z_id=0
        f_count+=1
"""
folder = "E:/Histopathology/Dataset/Renamed Data/T-25-22 adeno CA"
original = "E:/Histopathology/Dataset/Renamed Data/T-25-22 adeno CA/001-40x.tif"
zoomed = "E:/Histopathology/Dataset/Renamed Data/T-25-22 adeno CA/001-400x.tif"


from skimage.io import imread, imshow,imsave
from skimage.transform import rescale
def locate(original, zoomed, z=2.5):
    orig = imread(original)
    orig_crop = orig[14:2734,12:3572,:]
    #print(orig.shape, orig_crop.shape)
    
    zoom = imread(zoomed)
    zoom_crop = zoom[14:2734,12:3572,:]
    zoom_rescaled = rescale(zoom_crop,scale=1/z, multichannel=True)
    
    scale_factor = [40,8,4,2,1]
    
    for scale in scale_factor:
        orig_sc = rescale(orig_crop,scale=1/scale, multichannel=True)
        zoom_sc = rescale(zoom_rescaled,scale=1/scale, multichannel=True)
        if scale==40:
            oh,ow,_= orig_sc.shape
            zh,zw,_= zoom_sc.shape
            min = None
            posx, posy = 0,0
            for i in range(zh//2,oh-(zh//2)):
                for j in range(zw//2,ow-(zw//2)):
                    region = orig_sc[i-zh//2:i+zh//2,j-zw//2:j+zw//2,:]
                    if zoom_sc.shape[0]>region.shape[0]:
                        zoom_sc = zoom_sc[:-1,:,:]
                    if zoom_sc.shape[1]>region.shape[1]:
                        zoom_sc = zoom_sc[:,:-1,:]
                    if min == None :
                        min = (abs(zoom_sc-region)).sum()
                        posx,posy=i,j
                    elif (abs(zoom_sc-region)).sum()<min:
                        min = (abs(zoom_sc-region)).sum()
                        posx,posy=i,j
                   
            final_crop = orig_sc[posx-zh//2:posx+zh//2,posy-zw//2:posy+zw//2,:]
            imsave("E:/Histopathology/Dataset/Final Dataset/orig.png", orig_sc)
            imsave("E:/Histopathology/Dataset/Final Dataset/zoom.png", zoom_sc)
            imsave("E:/Histopathology/Dataset/Final Dataset/region.png",final_crop)
        else:
            if scale == 8:
                posx = 5*posx
                posy = 5*posy
            else:
                posx = 2*posx
                posy = 2*posy
            oh,ow,_= orig_sc.shape
            zh,zw,_= zoom_sc.shape
            min = None
            new_posx, new_posy = 0,0
            for i in range(posx-2,posx+3):
                for j in range(posy-2,posy+3):
                    print(posx, posy, i,j,zh,zw,i-zh//2,i+zh//2,j-zw//2,j+zw//2)
                    region = orig_sc[i-zh//2:i+zh//2,j-zw//2:j+zw//2,:]
                    if zoom_sc.shape[0]>region.shape[0]:
                        zoom_sc = zoom_sc[:-1,:,:]
                    if zoom_sc.shape[1]>region.shape[1]:
                        zoom_sc = zoom_sc[:,:-1,:]
                    if min == None :
                        min = (abs(zoom_sc-region)).sum()
                        new_posx,new_posy=i,j
                    elif (abs(zoom_sc-region)).sum()<min:
                        min = (abs(zoom_sc-region)).sum()
                        new_posx,new_posy=i,j
            posx,posy = new_posx,new_posy
    final_crop = orig_sc[posx-zh//2:posx+zh//2,posy-zw//2:posy+zw//2,:]

    return(final_crop)

out = locate(original, zoomed, 10)
imsave("E:/Histopathology/Dataset/Final Dataset/orig.png", imread(original))
imsave("E:/Histopathology/Dataset/Final Dataset/zoom.png", imread(zoomed))
imsave("E:/Histopathology/Dataset/Final Dataset/region.png",out)
