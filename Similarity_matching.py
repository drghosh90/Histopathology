import torch
from tqdm import tqdm
import torch.nn.functional as F
from PIL import Image
import torchvision
import numpy as np
import matplotlib.pyplot as plt

def transformation400(image_path, size):
    img = Image.open(image_path)
    transforms = torchvision.transforms.Compose([
        #torchvision.transforms.CenterCrop(int(size+.3*size)),
        torchvision.transforms.Resize((size,size)),
        torchvision.transforms.ToTensor(),
    ])
    img = transforms(img)
    return img
def transformation40_100(image_path, size):
    img = Image.open(image_path)
    transforms = torchvision.transforms.Compose([
        torchvision.transforms.Resize((size,size)),
        torchvision.transforms.ToTensor(),
    ])
    img = transforms(img)
    return img
def dataset_gen(img1_path,img2_path,output_path):
    
    
    img1 = transformation400(img1_path, 640)
    img2 = transformation40_100(img2_path, 2560)
    # print(img1.shape, img2.shape)
    
    image1 = transformation400(img1_path, 80)
    image2 = transformation40_100(img2_path, 320)

    image_size=320
    patch_size=80
    
    min_abs_value = float('inf')
    min_abs_region = None

    # Iterate over the image using sliding windows
    for i in tqdm(range(0, image_size - patch_size + 1, 1)):
        for j in range(0, image_size - patch_size + 1,1):
            # Extract the region from the image
            region = image2[:, i:i+patch_size, j:j+patch_size]
            # Compute the absolute difference between the region and the first image
            #print(image1.size())
            abs_diff = torch.abs(region - image1)

            # Calculate the sum of absolute differences
            sum_abs_diff = torch.mean(torch.sum(abs_diff))
            #print(torch.mean(sum_abs_diff))
            # Check if the current region has a smaller absolute difference
            if sum_abs_diff < min_abs_value:
                min_abs_value = sum_abs_diff
                min_abs_region = region
                min_abs_coordinate=(i,j)
                
    # print(min_abs_value)
    # print(min_abs_coordinate)

    crop_region = img2[:, min_abs_coordinate[0]*8:8*(min_abs_coordinate[0]+patch_size),
                8*min_abs_coordinate[1]:8*(min_abs_coordinate[1]+patch_size)]

    # Convert the cropped region tensor to numpy array for visualization
    crop_region_np = crop_region.numpy()

    # Show the cropped region
    plt.imshow(crop_region_np.transpose(1, 2, 0))
    plt.axis('off')
    #plt.show()

    t=crop_region_np.transpose(1, 2, 0)
    random_array = t*255
    random_array = random_array.astype(np.uint8)
    crop_image = Image.fromarray(random_array)
    #crop_image=crop_image.resize((256,256))
    # Save the cropped image
    crop_image.save(output_path)
    #Print the minimum absolute value and the corresponding region
    # print("Minimum Absolute Value:", min_abs_value)
    # print("Region with Minimum Absolute Value:")
    # print(min_abs_region)
    # print(min_abs_coordinate)
    
img1="Histopathology\Dataset\Renamed Data\T-19-22 ductal CA\\4.2.4.png" #400X
img2="Histopathology\Dataset\Renamed Data\T-19-22 ductal CA\\4.2.0.png" #100x# Constant
output="Histopathology\Dataset\Final Dataset\T-19-22 ductal CA\\4.0.2.4.png"



dataset_gen(img1,img2,output)
"""These are 400X times zoomed images extracted from 40X and 100X images via cropping"""



# import os
# file=[]
# ouput="Histopathology/Dataset/Final Dataset/T 26A-22 ductal CA"
# input_folder="D:\All-Projects\Super Resolution Dataset Generator\Histopathology\Dataset\Renamed Data\T 26A-22 ductal CA"

# for i in os.listdir(input_folder):
#     file.append(i)

#print(file)

# for 400X from 40X -->
# for i in range(1,len(file)-1,1):
#     #print(file[i])
#         dataset_gen(os.path.join(input_folder,file[i+1]),os.path.join(input_folder,file[i]),os.path.join(ouput,file[i]))
#         #print(os.path.join(ouput,file[i+1]))
#         #break
        
#for 400X from 100X -->
# for i in range(1,len(file)-1,1):
#     #print(file[i])
#         dataset_gen(os.path.join(input_folder,file[i]),os.path.join(input_folder,file[i+1]),os.path.join(ouput,file[i+1]))
#         #break
