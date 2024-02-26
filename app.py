from flask import Flask, request, render_template, jsonify
import base64
from PIL import Image
from io import BytesIO

import double_jpeg_compression

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('history.html')

@app.route('/detect')
def detect():
    return render_template('detect.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/processCompressDetection', methods=['POST'])
def processCompressDetection():
    try:
        if 'image' not in request.files:
            return jsonify({'status': False, 'message': 'No image file provided'})

        file = request.files['image']
        
        double_compressed = double_jpeg_compression.detect(file.filename)
        
        if double_compressed:
            return jsonify({'status': True, 'message': 'The image is double compressed.'})
        else:
            return jsonify({'status': False, 'message': 'The image is single compressed.'})

    except Exception as e:
        return jsonify({'status': False, 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
