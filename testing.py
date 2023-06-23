import torch 
import torchvision 
from PIL import Image
import os

input_path='Histopathology\Dataset\Renamed Data\Helping folder'
output_path='Histopathology\Dataset\Final Dataset\T-19-22 ductal CA'
tranform=torchvision.transforms.Compose([
    torchvision.transforms.Resize((2560,2560))
])

def resize_only(img_path,file_save_name):
    image=Image.open(img_path)
    image=tranform(image)
    image.save(os.path.join(output_path,'4.0.0.'+file_save_name+'_400X.png'))

a=1
for i in os.listdir(input_path):
    resize_only(os.path.join(input_path,i),str(a))
    a=a+1
    # break