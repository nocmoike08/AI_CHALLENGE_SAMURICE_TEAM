import tensorflow as tf
from tensorflow.keras import layers, models
import os

# Dataset path
dataset_dir = r'C:\Users\PC\Documents\Zalo Received Files\project-5-at-2025-05-11-13-43-7b83d22c\Canteen_Crops'
img_size = (128, 128)
batch_size = 64
train_ds = tf.keras.utils.image_dataset_from_directory(
    dataset_dir,
    image_size=img_size,
    batch_size=batch_size,
    shuffle=True
)

class_names = train_ds.class_names
print("Classes:", class_names)
normalization_layer = layers.Rescaling(1./255)
model = models.Sequential([
    normalization_layer,
    layers.Conv2D(32, (3,3), activation='relu', input_shape=img_size+(3,)),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(128, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(len(class_names), activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

epochs = 20
history = model.fit(train_ds, epochs=epochs)
model.save("food_cnn_model.h5")
