import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
from pathlib import Path

# モデルの読み込み
model = load_model('lon_san_model.h5')

# テスト画像のベースパス
test_dir = 'lon_san_dataset/test'
classes = ['lon', 'san']

# 結果記録
results = []
correct = 0
total = 0

for label in classes:
    folder = os.path.join(test_dir, label)
    for fname in os.listdir(folder):
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        img_path = os.path.join(folder, fname)
        img = image.load_img(img_path, target_size=(150, 150))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        pred = model.predict(img_array)[0][0]
        predicted_label = 'san' if pred > 0.5 else 'lon'

        is_correct = (predicted_label == label)
        if is_correct:
            correct += 1
        total += 1

        results.append((fname, label, predicted_label, pred, is_correct))

# 出力
for r in results:
    print(f"{r[0]} | 正解: {r[1]:<3} | 予測: {r[2]:<3} | 確信度: {r[3]:.2f} | {'✅' if r[4] else '❌'}")

accuracy = correct / total if total > 0 else 0
print(f"\n✅ 精度（accuracy）: {accuracy:.2%} ({correct}/{total})")


import matplotlib.pyplot as plt

# ❌ 間違えた画像のみを集めて表示
mistakes = [r for r in results if not r[4]]

if mistakes:
    print(f"\n❌ 間違えた画像一覧（{len(mistakes)}枚）")

    cols = 3
    rows = (len(mistakes) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))

    for idx, (fname, label, predicted_label, pred_score, _) in enumerate(mistakes):
        img_path = os.path.join(test_dir, label, fname)
        img = Image.open(img_path)
        ax = axes[idx // cols][idx % cols] if rows > 1 else axes[idx % cols]
        ax.imshow(img)
        ax.set_title(f"{fname}\n正解:{label} / 予測:{predicted_label} ({pred_score:.2f})")
        ax.axis('off')

    # 空白のサブプロットがある場合は非表示にする
    for i in range(len(mistakes), rows * cols):
        ax = axes[i // cols][i % cols] if rows > 1 else axes[i % cols]
        ax.axis('off')

    plt.tight_layout()
    plt.show()
else:
    print("\n🎉 全て正解でした！")