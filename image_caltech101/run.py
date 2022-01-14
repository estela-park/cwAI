## trouble shooting
## flow_from_directory 까지 debugged
## The use of `load_img` requires PIL=>requirements image 추가
## Image transformations require SciPy=>requirements scipy 추가
## => it stucks at gdown, downloaded not printing=>requirements numpy 순서, 버전 수정
## => numpy 지움: worked
## tensorflow==2.4.1, compatibility checked, numpy automatically installed
## =>docker push without downloading files, local training with downloading

import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from keras_preprocessing import image as Image
import gdown
import pathlib
import os
import tarfile
# import scipy


cwd = str(pathlib.Path().resolve())
print('running at', cwd)
data_path = cwd + '/data'

def createFolder(dir_name):
    try:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print('Directory has been made to', dir_name)
    except OSError:
        print ('Error: Creating directory:' +  dir_name)
        
print('will create dir at:', data_path)        
createFolder(data_path)

filename = data_path + '/101_ObjectCategories.tar.gz'

if os.path.exists(data_path):
    gdown.download('https://drive.google.com/u/0/uc?id=137RyRjvTBkBiIfeYBNZBtViDHQ6_Ewsp&export=download', filename, quiet=False)
    print('downloaded:', filename)

# print(filename)
with tarfile.open(filename) as f:
    f.extractall(data_path)
    extract_path = data_path + '/101_ObjectCategories'
    print('extracted the tar file')
    f.close()
    # at working directory, dir: 101_ObjectCategories> 101 sub dirs

print('If there is dir to work on:',os.path.exists(extract_path))

train_datagen = Image.ImageDataGenerator(
    rescale=1./255,
    horizontal_flip=True,
    vertical_flip=True,
    width_shift_range=0.1,
    height_shift_range=0.1,
    rotation_range=5,
    zoom_range=1.2,
    shear_range=0.7,
    fill_mode='nearest',
)

xy_train = train_datagen.flow_from_directory(
    extract_path,
    target_size=(224, 224),
    batch_size=10000,
    class_mode='categorical',
)
# Found 9144 images belonging to 102 classes.
# 101 things + 1 background

# print(xy_train[285][1].shape)
# [:284] = ([32, 224, 224, 3], [32, 102]), 3==color, 101==class_num
# [285]  = ([24, 224, 224, 3], [24, 102])
# print(xy_train[285][1][:][1])
# 102 class one-hot label

print('image has been revised')

x_train = xy_train[0][0]
y_train = xy_train[0][1]

print(type(x_train))
print(type(y_train))

print(x_train.shape)
print(y_train.shape)

# x_train: (9144, 224, 224, 3)
# y_train: (9144, 102)

# print(tf.reduce_sum(y_train, axis=0))
# tf.Tensor(
# [467. 435. 435. 200. 798.  55. 800.  42.  42.  47.  54.  46.  33. 128.
#  98.  43.  85.  91.  50.  43. 123.  47.  59.  62. 107.  47.  69.  73.
#  70.  50.  51.  57.  67.  52.  65.  68.  75.  64.  53.  64.  85.  67.
#  67.  45.  34.  34.  51.  99. 100.  42.  54.  88.  80.  31.  64.  86.
# 114.  61.  81.  78.  41.  66.  43.  40.  87.  32.  76.  55.  35.  39.
#  47.  38.  45.  53.  34.  57.  82.  59.  49.  40.  63.  39.  84.  57.
#  35.  64.  45.  86.  59.  64.  35.  85.  49.  86.  75. 239.  37.  59.
#  34.  56.  39.  60.], shape=(102,), dtype=float32)

# model = tf.keras.models.Sequential([
#   tf.keras.layers.Input(shape=(224,224,3)), 
#   tf.keras.layers.Conv2D(filters=64, kernel_size=(3,3), activation='relu', kernel_initializer='he_uniform'),
#   tf.keras.layers.Conv2D(filters=64, kernel_size=(3,3), activation='relu', kernel_initializer='glorot_normal'),
#   tf.keras.layers.MaxPool2D(pool_size=(2,2)),

#   tf.keras.layers.Conv2D(filters=128, kernel_size=(3,3), activation='relu', kernel_initializer='he_uniform'),
#   tf.keras.layers.Conv2D(filters=128, kernel_size=(3,3), activation='relu', kernel_initializer='glorot_normal'),
#   tf.keras.layers.Conv2D(filters=128, kernel_size=(3,3), activation='relu', kernel_initializer='glorot_normal'),
#   tf.keras.layers.MaxPool2D(pool_size=(2,2)),
#   tf.keras.layers.Dropout(0.35),

#   tf.keras.layers.Conv2D(filters=512, kernel_size=(3,3), activation='relu', kernel_initializer='he_uniform'),
#   tf.keras.layers.Conv2D(filters=128, kernel_size=(3,3), activation='relu', kernel_initializer='glorot_normal'),
#   tf.keras.layers.Conv2D(filters=128, kernel_size=(3,3), activation='relu', kernel_initializer='glorot_normal'),
#   tf.keras.layers.MaxPool2D(pool_size=(2,2)),
#   tf.keras.layers.Dropout(0.35),
  
#   tf.keras.layers.Conv2D(filters=256, kernel_size=(3,3), activation='relu', kernel_initializer='glorot_normal'),
#   tf.keras.layers.Conv2D(filters=256, kernel_size=(3,3), activation='relu', kernel_initializer='glorot_normal'),
#   tf.keras.layers.MaxPool2D(pool_size=(2,2)),
#   tf.keras.layers.Dropout(0.35),

#   tf.keras.layers.Conv2D(filters=512, kernel_size=(3,3), activation='relu', kernel_initializer='glorot_normal'),
#   tf.keras.layers.Conv2D(filters=512, kernel_size=(3,3), activation='relu', kernel_initializer='glorot_normal'),
#   tf.keras.layers.MaxPool2D(pool_size=(2,2)),
#   tf.keras.layers.Dropout(0.35),
  
#   tf.keras.layers.Flatten(),
#   tf.keras.layers.Dense(256, activation='relu'),
#   tf.keras.layers.Dropout(0.35), 
#   tf.keras.layers.Dense(128, activation='relu'),
#   tf.keras.layers.Dropout(0.35), 
#   tf.keras.layers.Dense(128, activation='relu'),
#   tf.keras.layers.Dropout(0.35), 
#   tf.keras.layers.Dense(102)
# ])

model_transfer = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
model_transfer.trainable = False

model = tf.keras.models.Sequential()
model.add(model_transfer)
model.add(tf.keras.layers.GlobalAveragePooling2D())
model.add(tf.keras.layers.Dense(512, activation='relu'))
model.add(tf.keras.layers.Dropout(0.15))
model.add(tf.keras.layers.Dense(256, activation='relu'))
model.add(tf.keras.layers.Dropout(0.15))
model.add(tf.keras.layers.Dense(128, activation='relu'))
model.add(tf.keras.layers.Dropout(0.25))
model.add(tf.keras.layers.Dense(102, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.summary()

from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
es = EarlyStopping(monitor='val_loss', patience=6, mode='min', verbose=2, restore_best_weights=True)
lr = ReduceLROnPlateau(monitor='val_loss', patience=4, mode='auto', verbose=2, factor=0.5)

hist = model.fit(x_train, y_train, epochs=180, validation_split=0.15, shuffle=True, callbacks=[es, lr], batch_size=32)
print(hist)