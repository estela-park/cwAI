import tensorflow as tf
from matplotlib import pyplot as plt


mnist = tf.keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# print(train_images.shape)
# 흑백 28x28

# plt.figure()
# plt.imshow(train_images[0])
# plt.colorbar()
# plt.grid(False)
# plt.show()
# max = 255.0

# Normalizing the image
train_images = train_images / 255.0
test_images = test_images / 255.0


# Modelling
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10)
])


# Compilation: using sparse obj fn, since pred is not one-hot encoded
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])


# Training
model.fit(train_images, train_labels, epochs=10, batch_size=64)


# Evaluation
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
print('\nTest accuracy:', test_acc)