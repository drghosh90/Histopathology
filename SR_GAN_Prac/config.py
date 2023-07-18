import torch
from PIL import Image
import torchvision.transforms

LOAD_MODEL = True
SAVE_MODEL = True
CHECKPOINT_GEN = "gen.pth.tar"
CHECKPOINT_DISC = "disc.pth.tar"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
LEARNING_RATE = 1e-4
NUM_EPOCHS = 100
BATCH_SIZE = 16
NUM_WORKERS = 4
HIGH_RES = 384
LOW_RES = HIGH_RES // 4
IMG_CHANNELS = 3

highres_transform = torchvision.transforms.Compose(
    [
        
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ]
)

lowres_transform = torchvision.transforms.Compose(
    [
        torchvision.transforms.Resize((LOW_RES,LOW_RES)),
        torchvision.transforms.Normalize(mean=[0, 0, 0], std=[1, 1, 1]),
        torchvision.transforms.ToTensor(),
    ]
)

both_transforms = torchvision.transforms.Compose(
    [
        torchvision.transforms.RandomCrop((HIGH_RES, HIGH_RES)),
        torchvision.transforms.RandomHorizontalFlip(p=0.5),
        torchvision.transforms.RandomRotation(.5),
    ]
)

test_transform = torchvision.transforms.Compose(
    [
        torchvision.transforms.Normalize(mean=[0, 0, 0], std=[1, 1, 1]),
        torchvision.transforms.ToTensor(),
    ]
)
