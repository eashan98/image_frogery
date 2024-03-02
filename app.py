from flask import Flask, request, render_template, jsonify
import base64
from PIL import Image
from io import BytesIO
from werkzeug.utils import secure_filename
import os
from datetime import datetime

import double_jpeg_compression
import image_extraction
import image_meta_data_extraction

app = Flask(__name__)

app.config['INPUT_DIR'] = 'static/input/images'
app.config['OUTPUT_DIR'] = 'static/output/images'

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
        
        if file.filename == '':
            return jsonify({'status': False, 'message': 'Invalid Image File.'})
                
        original_filename = secure_filename(file.filename)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{original_filename}"
        
        file.save(os.path.join(app.config['INPUT_DIR'], filename))
        
        double_compressed = double_jpeg_compression.detect(app.config['INPUT_DIR'],app.config['OUTPUT_DIR'], filename)
        
        if double_compressed:
            return jsonify({'status': True, 'message': 'The image is double compressed.'})
        else:
            return jsonify({'status': False, 'message': 'The image is single compressed.'})

    except Exception as e:
        return jsonify({'status': False, 'message': str(e)})
    

@app.route('/processMetaDataAnalysis', methods=['POST'])
def processMetaDataAnalysis():
    try:
        if 'image' not in request.files:
            return jsonify({'status': False, 'message': 'No image file provided'})

        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'status': False, 'message': 'Invalid Image File.'})
                
        original_filename = secure_filename(file.filename)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{original_filename}"
        
        file.save(os.path.join(app.config['INPUT_DIR'], filename))
                
        image_meta_data_extracted = image_meta_data_extraction.detect(app.config['INPUT_DIR'],app.config['OUTPUT_DIR'], filename)
        
        print(image_meta_data_extracted)
        
        if image_meta_data_extracted:
            return jsonify({'status': True, 'message': image_meta_data_extracted})
        else:
            return jsonify({'status': False, 'message': 'No Mata Data Associated With Image.'})

    except Exception as e:
        return jsonify({'status': False, 'message': str(e)})
    

@app.route('/processImageExtraction', methods=['POST'])
def processImageExtraction():
    try:
        if 'image' not in request.files:
            return jsonify({'status': False, 'message': 'No image file provided'})

        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'status': False, 'message': 'Invalid Image File.'})
                
        original_filename = secure_filename(file.filename)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{original_filename}"
        
        file.save(os.path.join(app.config['INPUT_DIR'], filename))
                
        image_extracted = image_extraction.detect(app.config['INPUT_DIR'],app.config['OUTPUT_DIR'], filename)
        
        if image_extracted:
            return jsonify({'status': True, 'message': 'Image extracted successfully.', 'image': os.path.join(app.config['OUTPUT_DIR'], filename)})
        else:
            return jsonify({'status': False, 'message': 'Image extraction failed due to some error.'})

    except Exception as e:
        return jsonify({'status': False, 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
