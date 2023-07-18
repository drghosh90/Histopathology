import os
import config
from PIL import Image
hr_dir="SR_GAN_Prac\Data\HR"
lr_dir="SR_GAN_Prac\Data\LR"

hr_files=os.listdir(hr_dir)
# print(os.listdir(hr_dir))
file=os.path.join(hr_dir,hr_files[0])
high_res=Image.open(file)

high_res=config.highres_transform(high_res)
