from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow import keras
import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageChops
import json
import io
import base64

app = Flask(__name__)
CORS(app)

model = keras.models.load_model('model/mnist_model.h5')
print("✅ Model loaded successfully.")

def trim(im):
    bg = Image.new(im.mode, im.size, 0)
    diff = ImageChops.difference(im, bg)
    if not diff.getbbox():
        return None 
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        drawing_data = json.loads(data['imageData'])
        img_user = Image.new('L', (280, 280), 'white')
        draw = ImageDraw.Draw(img_user)
        for line in drawing_data['lines']:
            points = [tuple(p.values()) for p in line['points']]
            draw.line(points, fill='black', width=int(line['brushRadius'] * 2))
        img_inverted = ImageOps.invert(img_user)
        img_trimmed = trim(img_inverted)

        if img_trimmed is None:
            return jsonify({'prediction': 'N/A'})

        
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

if __name__ == '__main__':
    app.run(port=5000)