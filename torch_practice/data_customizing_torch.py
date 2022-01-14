from .customdataset_torch import FaceLandmarksDataset
from .transform_torch import Rescale, RandomCrop, ToTensor
from torchvision import transforms
import cv2 


transformed_dataset = FaceLandmarksDataset(csv_file='img_annotation.csv',
                                           root_dir='directory_path_where imgs are',
                                           transform=transforms.Compose([
                                               Rescale(64),
                                               RandomCrop(32),
                                               ToTensor()
                                           ]))

for i in range(len(transformed_dataset)):
    sample = transformed_dataset[i]
    cv2.imshow(sample)