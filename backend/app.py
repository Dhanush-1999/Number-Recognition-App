from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow import keras
import numpy as np
from PIL import Image, ImageOps, ImageChops
import base64
import io

app = Flask(__name__)
CORS(app)

model = keras.models.load_model('mnist_model.h5')
print("✅ Model loaded successfully.")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        image_data_url = data['imageData']
        
        image_data = base64.b64decode(image_data_url.split(',')[1])
        image_opened = Image.open(io.BytesIO(image_data))

        background = Image.new('RGB', image_opened.size, 'white')
        
        if image_opened.mode == 'RGBA':
            background.paste(image_opened, mask=image_opened.split()[3])
        else:
            background.paste(image_opened)
        
        image_gray = background.convert('L')
        
        image_resized = image_gray.resize((28, 28))
        
        image_array = np.array(image_resized)
        
        image_array = (255.0 - image_array) / 255.0
        image_reshaped = image_array.reshape(1, 28, 28, 1)
        
        prediction = model.predict(image_reshaped)
        predicted_digit = int(np.argmax(prediction))
        
        return jsonify({'prediction': predicted_digit})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)