import torch
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt


image_path = 'Histopathology\Dataset\Testing Data\LR\\001-100x.tif'

# Patch Divider
def divide_image_into_patches(image, patch_size, overlap_ratio):
    width, height = image.size
    stride = int(patch_size * (1 - overlap_ratio))

    patches = []
    for y in range(0, height - patch_size + 1, stride):
        for x in range(0, width - patch_size + 1, stride):
            patch = image.crop((x, y, x + patch_size, y + patch_size))
            patches.append(patch)

    return patches

# Load the image using Pillow (replace 'path_to_your_image.jpg' with the actual path)

image = Image.open(image_path)

# Patch Blender

def blend_patches(patches, image_size, patch_size, overlap_ratio):
    canvas = Image.new("RGB", image_size)

    width, height = image_size
    stride = int(patch_size * (1 - overlap_ratio))

    patch_counts = [[1 for _ in range(width)] for _ in range(height)]

    for i, patch in enumerate(patches):
        x_start = (i % (width // stride)) * stride
        y_start = (i // (width // stride)) * stride

        for y in range(patch_size):
            for x in range(patch_size):
                r, g, b = patch.getpixel((x, y))
                r_prev, g_prev, b_prev = canvas.getpixel((x_start + x, y_start + y))
                r_avg = (r + r_prev) / patch_counts[y_start + y][x_start + x]
                g_avg = (g + g_prev) / patch_counts[y_start + y][x_start + x]
                b_avg = (b + b_prev) / patch_counts[y_start + y][x_start + x]
                canvas.putpixel((x_start + x, y_start + y), (int(r_avg), int(g_avg), int(b_avg)))
                patch_counts[y_start + y][x_start + x] += 1

    return canvas

# Load the image using Pillow (replace 'path_to_your_image.jpg' with the actual path)
image = Image.open(image_path)


# Define patch size and overlap ratio
patch_size = image.size[0]//10
overlap_ratio = 0.0

# Divide the image into overlapping patches
patches = divide_image_into_patches(image, patch_size, overlap_ratio)
# Display the image patches
num_patches = len(patches)
rows = (num_patches - 1) // 5 + 1
for i, patch in enumerate(patches):
    plt.subplot(rows, 5, i + 1)
    plt.imshow(patch)
    # plt.title(f'Patch {i+1}')
    plt.axis('off')
plt.show()



# Blend the overlapping patches to create a new image
new_image = blend_patches(patches, image.size, patch_size, overlap_ratio)
# Display the new blended image
new_image.show()