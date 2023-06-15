import os
from skimage.io import imread,imsave
import cv2
from skimage.transform import resize
path = "D:/Codes/Histopathology/Dataset/Renamed Data/T 26A-22 ductal CA"
savepath = "D:/Codes/Histopathology/Dataset/Final Dataset"

def locate400in100(img400, img100):
    miniimg400 = resize(img400, (64,64,3))
    miniimg100 = resize(img100, (275,358,3))
    x,y = minimatch(miniimg400,miniimg100)
    x,y = 10*x, 10*y
    cropped_img = bigmatch(img400, img100, x, y)
    imsave(savepath+'/100x.png'+cropped_img)
    imsave(savepath+'/400x.png'+img400)

def bigmatch(small, large, px, py):
    sx,sy,_ = small.shape 
    lx,ly,_ = large.shape
    min = None
    for i in range (px-10, px+10):
        for j in range(py-10, py+10):
            print(i-(sx//2),i+(sx//2),j-(sy//2),j+(sy//2))
            newdiff = small - large[i-(sx//2):i+(sx//2),j-(sy//2):j+(sy//2),:]
            if min==None:
                diff = newdiff
                x,y=i,j
            else:
                if diff>newdiff:
                    diff=newdiff
                    x,y = i,j
    return(large[x-(sx//2):x+(sx//2),y-(sy//2):y+(sy//2),:])

def minimatch(small, large):
    sx,sy,_ = small.shape 
    lx,ly,_ = large.shape
    min = None
    for i in range (sx//2, lx-(sx//2)):
        for j in range(sy//2, ly-(sy//2)):
            newdiff = small - large[i-(sx//2):i+(sx//2),j-(sy//2):j+(sy//2),:]
            if min==None:
                diff = newdiff
                x,y=i,j
            else:
                if diff>newdiff:
                    diff=newdiff
                    x,y = i,j
    return(x,y)

for i in range(1,11):
    #img_40x = imread("%s/%03d-40x.tif"%(path, i))
    img_100x = cv2.imread("%s/%03d-100x.tif"%(path, i))
    print("%s/%03d-400x.tif"%(path, i))
    img_400x = cv2.imread("%s/%03d-400x.tif"%(path, i))
    h,w,_ = img_400x.shape
    img_400x = img_400x[(h-2560)//2:2560+((h-2560)//2),(w-2560)//2:2560+((w-2560)//2),:]
    cropped_img_100x= locate400in100(img_400x, img_100x)
    #locate400in40()