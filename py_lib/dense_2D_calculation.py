import tensorflow as tf
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


x = np.array([[ [1, 2, 3],
                [1, 2, 3],
                [1, 2, 3]],
              [ [3, 5, 7],
                [3, 5, 7],
                [3, 5, 7]],
              [ [11, 13, 17],
                [11, 13, 17],
                [11, 13, 17]]])
print(x.shape)

y = np.array([[1], [0], [1]])

model = Sequential()
model.add(Dense(3, input_shape=(3, 3)))
model.add(Dense(1, activation='sigmoid'))

model.summary()

model.compile(optimizer='rmsprop', loss='binary_crossentropy')
hist = model.fit(x, y, epochs=32)

print(hist)