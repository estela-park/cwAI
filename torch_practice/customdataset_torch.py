from torch.utils.data import Dataset
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import torch
import os
import io

class FaceLandmarksDataset(Dataset):

    def __init__(self, csv_file, root_dir, transform=None):
        # csv_file: 이미지의 파일명, 어노테이션 내용(ex: landmarks)
        # root_dir: 이미지 디렉토리 경로
        
        self.landmarks_frame = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.landmarks_frame)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_name = os.path.join(self.root_dir,
                                self.landmarks_frame.iloc[idx, 0])
        image = io.imread(img_name)
        # skimage.io.imread 이미지 사이즈에 맞는 shape의 np.ndarray 반환
        # gray-image: MxN, RGB-image: MxNx3, RGBA-image: MxNx4
        # M, N은 픽셀의 갯수
        landmarks = self.landmarks_frame.iloc[idx, 1:]
        landmarks = np.array([landmarks])
        landmarks = landmarks.astype('float').reshape(-1, 2)
        # landmark를 (x, y)의 형태로 반환
        sample = {'image': image, 'landmarks': landmarks}

        if self.transform:
            sample = self.transform(sample)

        return sample


def show_landmarks(image, landmarks):
    plt.imshow(image)
    plt.scatter(landmarks[:, 0], landmarks[:, 1], s=10, marker='.', c='r')
    # landmark의 (x, y)값에 따라 size=10, 빨간 점을 찍는다(=scatter)
    plt.pause(0.001)  # pause a bit so that plots are updated
    
    
face_dataset = FaceLandmarksDataset(csv_file='data/faces/face_landmarks.csv',
                                    root_dir='data/faces/')

fig = plt.figure()

for i in range(len(face_dataset)):
    sample = face_dataset[i]

    print(i, sample['image'].shape, sample['landmarks'].shape)

    ax = plt.subplot(1, 4, i + 1)
    plt.tight_layout()
    ax.set_title('Sample #{}'.format(i))
    ax.axis('off')
    show_landmarks(**sample)

    if i == 3:
        plt.show()
        break