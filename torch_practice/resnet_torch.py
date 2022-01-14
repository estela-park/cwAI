## Resnet50 for mask/keypoint -RCNN

import torch
import torch.nn as nn

class block(nn.Module):
    def __init__(self, in_channels, intermediate_channels, identity_downsample=None, stride=1):
    # stride = 1    일반적인 feature extract
    # stride >= 2   img resolution 축소
    
        super(block, self).__init__()
        self.expansion = 4
        
        self.conv1 = nn.Conv2d(in_channels, intermediate_channels, kernel_size=1, stride=1, padding=0, bias=False)
        # 커널 사이즈 1x1의 경우 패딩 필요없음
        self.bn1 = nn.BatchNorm2d(intermediate_channels)
        
        self.conv2 = nn.Conv2d(intermediate_channels, intermediate_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(intermediate_channels)
        
        self.conv3 = nn.Conv2d(intermediate_channels, intermediate_channels*self.expansion, kernel_size=1, stride=1, padding=0, bias=False)
        self.bn3 = nn.BatchNorm2d(intermediate_channels*self.expansion)
        
        self.relu = nn.ReLU()
        self.identity_downsample = identity_downsample
        self.stride = stride
        
    def forward(self, x):
        # x는 이전 block의 output
        id = x.clone()
        
        x = self.conv1()
        x = self.bn1()
        x = self.relu()
        x = self.conv2()
        x = self.bn2()
        x = self.relu()
        x = self.conv3()
        x = self.bn3()

        if self.identity_downsample is not None:
        # ResNet 구조상 signal tensor의 shape나 channel수가 바뀔 수 있다
        # res block 끝 부분에서 skip connection을 통해 더하는 id tensor를 block 생성자의 arg로서 넣어준 경우, 
            id = self.identity_downsample(id)
            # 여기서 들어가는 id는 이전 블락의 output(=x).clone()
        
        x += id
        x = self.relu(x)
        # 마지막 활성화함수는 +id 이후에 적용한다
        
        return x
    
    
class ResNet(nn.Module):
# 구조: stem + res blocks[layer의 갯수는 모델에 따라 다르다]
    def __init__(self, block, layers, image_channels, num_classes):
        '''
        block = 
        layers = 
        image_channels = 흑백(=1) or 컬러(=3 or 4)
        num_classes = FC로 분류할 클래스 수, 최종 output dimension과 일치해야한다.
        '''
        super(ResNet, self).__init__()
        self.in_channels = 64
        
        # 아래는 stem block의 spec
        # stem block: 줄기세포처럼 특정한 기능을 갖지않고 Residual Block에 input하도록 data transformation
        # 결과적으로 이미지는 1/4 resolution, channel=64의 시그널로 전환된다.
        self.conv1 = nn.Conv2d(image_channels, 64, kernel_size=7, stride=2, padding=3, bias=False)
        # kernel, stride, padding 조합으로 img resolution 반으로 줄임
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        # kernel, stride, padding 조합으로 img resolution 반으로 줄임

        
        # 아래는 residual block의 구성
        self.layer1 = self._make_layer(block, layers[0], intermediate_channels=64, stride=1)
        self.layer2 = self._make_layer(block, layers[1], intermediate_channels=128, stride=2)
        self.layer3 = self._make_layer(block, layers[2], intermediate_channels=256, stride=2)
        self.layer4 = self._make_layer(block, layers[3], intermediate_channels=512, stride=2)