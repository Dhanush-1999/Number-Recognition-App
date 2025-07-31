import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from tensorflow import keras
import numpy as np
from PIL import Image, ImageOps, ImageChops
import json

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'mnist_model.h5')


app = Flask(__name__, static_folder='build/static')
CORS(app)

model = keras.models.load_model(MODEL_PATH)
print("✅ Model loaded successfully from:", MODEL_PATH)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        drawing_data = json.loads(data['drawingData'])
        
        img = Image.new('L', (280, 280), 'white')
        draw = ImageDraw.Draw(img)
        for line in drawing_data['lines']:
            points = [tuple(p.values()) for p in line['points']]
            draw.line(points, fill='black', width=int(line['brushRadius'] * 2))

        img_inverted = ImageOps.invert(img)
        
        bg = Image.new(img_inverted.mode, img_inverted.size, 0)
        diff = ImageChops.difference(img_inverted, bg)
        if not diff.getbbox():
            return jsonify({'prediction': 'N/A'})
        bbox = diff.getbbox()
        img_trimmed = img_inverted.crop(bbox)

        new_img = Image.new('L', (28, 28), 'black')
        img_resized = img_trimmed.copy()
        img_resized.thumbnail((20, 20), Image.Resampling.LANCZOS)
        offset_x = (28 - img_resized.width) // 2
        offset_y = (28 - img_resized.height) // 2
        new_img.paste(img_resized, (offset_x, offset_y))
        
        image_array = np.array(new_img) / 255.0
        image_reshaped = image_array.reshape(1, 28, 28, 1)
        
        prediction = model.predict(image_reshaped)
        predicted_digit = int(np.argmax(prediction))
        
        return jsonify({'prediction': predicted_digit})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and path != "favicon.ico":
        return send_from_directory('build', path)
    else:
        return send_from_directory('build', 'index.html')

if __name__ == '__main__':
    app.run(port=5000)