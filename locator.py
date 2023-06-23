import torch
from tqdm import tqdm
import torch.nn.functional as F
from PIL import Image
import torchvision
import numpy as np
import matplotlib.pyplot as plt

def transformation(image_path, size):
    img = Image.open(image_path)
    transforms = torchvision.transforms.Compose([
        #torchvision.transforms.CenterCrop(2748),
        torchvision.transforms.Resize((size,size)),
        torchvision.transforms.ToTensor(),
    ])
    img = transforms(img)
    return img

# def dataset_gen(img1_path,img2_path,output_path):
image1 = transformation("Histopathology/Dataset/Renamed Data/T 26A-22 ductal CA/005-400x.tif", 640)
image2 = transformation("Histopathology/Dataset/Renamed Data/T 26A-22 ductal CA/005-100x.tif", 2560)

image_size=2560
patch_size=640


min_abs_value = float('inf')
min_abs_region = None

# Iterate over the image using sliding windows
for i in tqdm(range(0, image_size - patch_size + 1, 20)):
    for j in range(0, image_size - patch_size + 1,20):
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
            
print(min_abs_value)
# print(min_abs_coordinate)

crop_region = image2[:, min_abs_coordinate[0]:min_abs_coordinate[0]+patch_size,
            min_abs_coordinate[1]:min_abs_coordinate[1]+patch_size]

# Convert the cropped region tensor to numpy array for visualization
crop_region_np = crop_region.numpy()

# Show the cropped region
plt.imshow(crop_region_np.transpose(1, 2, 0))
plt.axis('off')
plt.show()

t=crop_region_np.transpose(1, 2, 0)
random_array = t*255
random_array = random_array.astype(np.uint8)
crop_image = Image.fromarray(random_array)

# Save the cropped image
crop_image.save("D:\All-Projects\Super Resolution Dataset Generator\Histopathology\cropped_image.png")
#Print the minimum absolute value and the corresponding region
print("Minimum Absolute Value:", min_abs_value)
print("Region with Minimum Absolute Value:")
print(min_abs_region)
print(min_abs_coordinate)