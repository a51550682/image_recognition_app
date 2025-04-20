import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image
import numpy as np

# 加载 MobileNetV2 预训练模型
model = MobileNetV2(weights='imagenet')

def predict_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))  # 调整图片大小
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)  # 模型预测
    return decode_predictions(preds, top=3)[0]  # 返回 Top-3 预测结果
