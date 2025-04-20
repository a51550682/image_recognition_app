from flask import Flask, render_template, request, redirect, url_for 
from werkzeug.utils import secure_filename
import os
from model.model import predict_image

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return render_template('index.html', error="文件類型無效！請上傳圖片。")
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    predictions = predict_image(filepath)[:3]  # ✅ 顯示 Top-3
    return render_template('index.html', filename=filename, predictions=predictions)

@app.route('/delete/<filename>', methods=['POST'])
def delete_image(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        os.remove(filepath)
        return redirect(url_for('index'))
    except Exception as e:
        return render_template('index.html', error=f"刪除失敗：{e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
