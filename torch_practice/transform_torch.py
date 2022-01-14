# transforms.Compose[*]
# * 자리에서 함수를 호출했을 때 이미지에 일련의 작업을 하도록 __call__함수를 구현한다.

from torchvision import transforms, utils
from skimage import io, transform
import matplotlib.pyplot as plt
import numpy as np
import torch


# data 구성
# image= human facial image
# landmarks= ficial landmarks such as tips of eyebrow, outer countour, etc
class Rescale(object):
    def __init__(self, output_size):
        assert isinstance(output_size, (int, tuple))
        self.output_size = output_size

    def __call__(self, sample):
        image, landmarks = sample['image'], sample['landmarks']

        # output_size는 int or tuple
        h, w = image.shape[:2]
        if isinstance(self.output_size, int):
        # output_size == int, 짧은 쪽을 맞추고 긴 쪽은 비례에 맞게 scaling
            if h > w:
                new_h, new_w = self.output_size * h / w, self.output_size
            else:
                new_h, new_w = self.output_size, self.output_size * w / h
        else:
            new_h, new_w = self.output_size

        new_h, new_w = int(new_h), int(new_w)

        img = transform.resize(image, (new_h, new_w))

        landmarks = landmarks * [new_w / w, new_h / h]
        # image는 h, w순의 축을 사용하고 landmark좌표는 x, y (axis=1, axis=0)을 사용한다.

        return {'image': img, 'landmarks': landmarks}


class RandomCrop(object):
# vision model의 성능을 향상시키기 위해 raw image의 부분을 잘라서 학습시킨다
# ex) 얼굴 반 쪽의 이미지만 보고도 사람으로 classifying 하도록 학습

    def __init__(self, output_size):
        assert isinstance(output_size, (int, tuple))
        if isinstance(output_size, int):
        # int로 size 넣어줄 경우, 정사각형 모양으로 자른다.
            self.output_size = (output_size, output_size)
        else:
            assert len(output_size) == 2
            self.output_size = output_size

    def __call__(self, sample):
        image, landmarks = sample['image'], sample['landmarks']

        h, w = image.shape[:2]
        new_h, new_w = self.output_size

        # assert h > new_h & w > new_w; 필요함!
        top = np.random.randint(0, h - new_h)
        left = np.random.randint(0, w - new_w)

        image = image[top: top + new_h,
                      left: left + new_w]
        # 이미지의 원래 크기에서 crop 지정 사이즈로 잘라낸다
        # 시작(범위내의 random int) ~ 시작 + size

        landmarks = landmarks - [left, top]
        # landmark 좌표축 평행이동, 범위 벗어나는 좌표가 생긴다

        return {'image': image, 'landmarks': landmarks}


class ToTensor(object):

    def __call__(self, sample):
        image, landmarks = sample['image'], sample['landmarks']

        # swap color axis because
        # numpy image: H x W x C
        # torch image: C X H X W
        # transpose는 np.transpose()
        image = image.transpose((2, 0, 1))
        return {'image': torch.from_numpy(image),
                'landmarks': torch.from_numpy(landmarks)}
        

# torchvision.transforms 사용하는 방식
scale = Rescale(256)
crop = RandomCrop(128)
composed = transforms.Compose([Rescale(256),
                               RandomCrop(224)])