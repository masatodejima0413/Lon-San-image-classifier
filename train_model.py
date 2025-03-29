import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import matplotlib.pyplot as plt
import random
import numpy as np
import tensorflow as tf

random.seed(42)
np.random.seed(42)
tf.random.set_seed(42)

# データセットのパス
base_dir = 'lon_san_dataset'
train_dir = os.path.join(base_dir, 'train')
val_dir = os.path.join(base_dir, 'val')

# データ拡張と正規化（0〜1にスケーリング）
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest'
)

val_datagen = ImageDataGenerator(rescale=1./255)

# 画像ジェネレータの作成
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(150, 150),
    batch_size=16,
    class_mode='binary'
)

val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=(150, 150),
    batch_size=16,
    class_mode='binary'
)

# モデル構築（CNN）
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(150, 150, 3)),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Conv2D(128, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Conv2D(128, (3,3), activation='relu'),         # ← 追加！
    MaxPooling2D(2,2),                              # ← 追加！
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# 学習
history = model.fit(
    train_generator,
    epochs=15,
    validation_data=val_generator
)

# モデルを保存する（1回だけでOK）
model.save('lon_san_model.h5')

plt.figure(figsize=(18, 5))  # 横長のウィンドウにする

# === グラフ1：train / val accuracy ===
plt.subplot(1, 3, 1)  # 1行3列のうち1枚目
plt.plot(history.history['accuracy'], label='train acc')
plt.plot(history.history['val_accuracy'], label='val acc')
plt.title('Accuracy')
plt.legend()

# === グラフ2：train / val loss ===
plt.subplot(1, 3, 2)  # 1行3列のうち2枚目
plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.title('Loss')
plt.legend()

# === グラフ3：val accuracy vs val loss の関係（おまけ）
plt.subplot(1, 3, 3)  # 1行3列のうち3枚目
plt.plot(history.history['val_accuracy'], label='val acc')
plt.plot(history.history['val_loss'], label='val loss')
plt.title('Val Accuracy vs Loss')
plt.legend()

plt.tight_layout()
plt.show()