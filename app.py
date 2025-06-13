from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
from PIL import Image

app = Flask(__name__)

# Load the models once at startup
suspicious_model = joblib.load('model/suspicious.pkl')
vectorizer = joblib.load('model/vectorizer.pkl')

@app.route('/')
def home():
    return render_template('index.html')

# ------------ TEXT Threat Detection ------------
@app.route('/predict-text', methods=['POST'])
def predict_text():
    try:
        data = request.get_json()
        user_text = data.get('message', '')

        if not user_text.strip():
            return jsonify({'error': 'No input provided'})

        vectorized = vectorizer.transform([user_text])
        prediction = suspicious_model.predict(vectorized)
        probability = suspicious_model.predict_proba(vectorized)[0][1] * 100  # Assuming binary classification
        return jsonify({'result': f'{probability:.2f}%'})
    except Exception as e:
        return jsonify({'error': str(e)})

# ------------ URL Threat Detection ------------
@app.route('/predict-url', methods=['POST'])
def predict_url():
    try:
        data = request.get_json()
        url_input = data.get('url', '')

        if not url_input.strip():
            return jsonify({'error': 'No URL provided'})

        vec_url = vectorizer.transform([url_input])
        prediction = suspicious_model.predict(vec_url)
        probability = suspicious_model.predict_proba(vec_url)[0][1] * 100  # Assuming binary classification
        return jsonify({'result': f'{probability:.2f}%'})
    except Exception as e:
        return jsonify({'error': str(e)})

# ------------ IMAGE Threat Detection ------------
@app.route('/predict-image', methods=['POST'])
def predict_image():
    try:
        image_file = request.files['image']
        image = Image.open(image_file.stream).convert("RGB")
        image = image.resize((224, 224))
        img_array = np.array(image).reshape(1, 224, 224, 3) / 255.0

        prediction = suspicious_model.predict(img_array)
        probability = suspicious_model.predict_proba(img_array)[0][1] * 100  # Assuming binary classification
        return jsonify({'result': f'{probability:.2f}%'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/about')  
def about():  
    return render_template('about.html')  

@app.route('/contact')  
def contact():  
    return render_template('contact.html')  

@app.route('/images')  
def images():  
    return render_template('images.html')  

@app.route('/links')  
def links():  
    return render_template('links.html')  

@app.route('/texts')  
def texts():  
    return render_template('texts.html')  
# The duplicate about function has been removed.

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
