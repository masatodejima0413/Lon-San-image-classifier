import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

# 保存されたモデルファイルを読み込む
model = load_model('lon_san_model.h5')

# 予測対象の画像パス（← ここは実際の画像に変えてください）
img_path = 'lon_san_dataset/test/lon/2019-10-05_01-12-18_669.jpg'

# 画像読み込みと前処理（リサイズ・正規化）
img = image.load_img(img_path, target_size=(150, 150))
img_array = image.img_to_array(img)
img_array = img_array / 255.0  # 正規化
img_array = np.expand_dims(img_array, axis=0)  # バッチ次元を追加

# 予測実行
prediction = model.predict(img_array)[0][0]

# 結果表示
plt.imshow(img)
plt.axis('off')
label = "san 🐯" if prediction > 0.5 else "lon 🐱"
plt.title(f"Predicted: {label} ({prediction:.2f})")
plt.show()