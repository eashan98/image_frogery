from flask import Flask, request, render_template, jsonify
import base64
from PIL import Image
from io import BytesIO
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from optparse import OptionParser

import double_jpeg_compression
import image_extraction
import image_meta_data_extraction
import cfa_artifact
import noise_inconsistency
import error_level_analysis
import string_extraction
import copy_move_detection

app = Flask(__name__)

app.config['INPUT_DIR'] = 'static/input/images'
app.config['OUTPUT_DIR'] = 'static/output/images'

cmd = OptionParser("usage: %prog image_file [options]")
cmd.add_option('', '--imauto',
               help='Automatically search identical regions. (default: %default)', default=1)
cmd.add_option('', '--imblev',
               help='Blur level for degrading image details. (default: %default)', default=8)
cmd.add_option('', '--impalred',
               help='Image palette reduction factor. (default: %default)', default=15)
cmd.add_option(
    '', '--rgsim', help='Region similarity threshold. (default: %default)', default=5)
cmd.add_option(
    '', '--rgsize', help='Region size threshold. (default: %default)', default=1.5)
cmd.add_option(
    '', '--blsim', help='Block similarity threshold. (default: %default)', default=200)
cmd.add_option('', '--blcoldev',
               help='Block color deviation threshold. (default: %default)', default=0.2)
cmd.add_option(
    '', '--blint', help='Block intersection threshold. (default: %default)', default=0.2)
opt, args = cmd.parse_args()

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
            return jsonify({'status': False, 'type':'danger', 'message': 'No Image Selected', 'data': 'No image file provided!'})

        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'status': False, 'type':'danger', 'message': 'Invalid Image', 'data': 'Invalid image file!'})
                
        original_filename = secure_filename(file.filename)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{original_filename}"
        
        file.save(os.path.join(app.config['INPUT_DIR'], filename))
        
        double_compressed = double_jpeg_compression.detect(app.config['INPUT_DIR'],app.config['OUTPUT_DIR'], filename)
        
        if double_compressed:
            return jsonify({'status': True, 'type':'danger', 'message': 'Double Compression Found', 'data': 'The image is double compressed!'})
        else:
            return jsonify({'status': False, 'type':'success', 'message': 'Single Compression Found', 'data': 'The image is single compressed!'})

    except Exception as e:
        return jsonify({'status': False, 'type':'danger', 'message': "Error Exception", 'data': str(e)})
    

@app.route('/processMetaDataAnalysis', methods=['POST'])
def processMetaDataAnalysis():
    try:
        if 'image' not in request.files:
            return jsonify({'status': False, 'type':'danger', 'message': 'No Image Selected', 'data': 'No image file provided!'})

        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'status': False, 'type':'danger', 'message': 'Invalid Image', 'data': 'Invalid image file!'})
                
        original_filename = secure_filename(file.filename)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{original_filename}"
        
        file.save(os.path.join(app.config['INPUT_DIR'], filename))
                
        image_meta_data_extracted = image_meta_data_extraction.detect(app.config['INPUT_DIR'],app.config['OUTPUT_DIR'], filename)
                
        if image_meta_data_extracted:
            return jsonify({'status': True, 'type':'success', 'message': 'Meta Data Found', 'data': image_meta_data_extracted})
        else:
            return jsonify({'status': True, 'type':'danger', 'message': 'No Mata Data Found', 'data': 'No mata data found associated with image!'})

    except Exception as e:
        return jsonify({'status': False, 'type':'danger', 'message': "Error Exception", 'data': str(e)})
    
    
@app.route('/processCfaArtifactDetection', methods=['POST'])
def processCfaArtifactDetection():
    try:
        if 'image' not in request.files:
            return jsonify({'status': False, 'type':'danger', 'message': 'No Image Selected', 'data': 'No image file provided!'})

        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'status': False, 'type':'danger', 'message': 'Invalid Image', 'data': 'Invalid image file!'})
                
        original_filename = secure_filename(file.filename)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{original_filename}"
        
        file.save(os.path.join(app.config['INPUT_DIR'], filename))
                
        image_cfa_artifact = cfa_artifact.detect(app.config['INPUT_DIR'],app.config['OUTPUT_DIR'], filename, opt, args)
                
        if image_cfa_artifact:
            return jsonify({'status': True, 'type':'danger', 'message': 'CFA Artifacts Detected', 'data': str(image_cfa_artifact) + ' CFA artifacts detected!', 'image': os.path.join(app.config['OUTPUT_DIR'], filename)})
        else:
            return jsonify({'status': True, 'type':'success', 'message': 'No CFA Artifacts Detected', 'data': 'No CFA artifacts detected!', 'image': os.path.join(app.config['OUTPUT_DIR'], filename)})

    except Exception as e:
        return jsonify({'status': False, 'type':'danger', 'message': "Error Exception", 'data': str(e)})
    
@app.route('/processNoiseInconsistency', methods=['POST'])
def processNoiseInconsistency():
    try:
        if 'image' not in request.files:
            return jsonify({'status': False, 'type':'danger', 'message': 'No Image Selected', 'data': 'No image file provided!'})

        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'status': False, 'type':'danger', 'message': 'Invalid Image', 'data': 'Invalid image file!'})
                
        original_filename = secure_filename(file.filename)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{original_filename}"
        
        file.save(os.path.join(app.config['INPUT_DIR'], filename))
                
        image_noise_inconsistency = noise_inconsistency.detect(app.config['INPUT_DIR'],app.config['OUTPUT_DIR'], filename)
                
        if image_noise_inconsistency:
            return jsonify({'status': True, 'type':'danger', 'message': 'Noise Inconsistency Found', 'data': 'Noise inconsistency found!'})
        else:
            return jsonify({'status': True, 'type':'success', 'message': 'No Noise Inconsistency Found', 'data': 'No noise inconsistency found with image!'})

    except Exception as e:
        return jsonify({'status': False, 'type':'danger', 'message': "Error Exception", 'data': str(e)})
    
@app.route('/processErrorLevelAnalysis', methods=['POST'])
def processErrorLevelAnalysis():
    try:
        if 'image' not in request.files:
            return jsonify({'status': False, 'type':'danger', 'message': 'No Image Selected', 'data': 'No image file provided!'})

        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'status': False, 'type':'danger', 'message': 'Invalid Image', 'data': 'Invalid image file!'})
                
        original_filename = secure_filename(file.filename)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{original_filename}"
        
        file.save(os.path.join(app.config['INPUT_DIR'], filename))
                
        image_error_level_analysis = error_level_analysis.detect(app.config['INPUT_DIR'],app.config['OUTPUT_DIR'], filename)
                
        if image_error_level_analysis:
            return jsonify({'status': True, 'type':'success', 'message': 'Image Error Level Analysis Completed', 'data': 'Image error level analysis completed successfuly!', 'image': os.path.join(app.config['OUTPUT_DIR'], filename)})
        else:
            return jsonify({'status': False, 'type':'danger', 'message': 'Image Error Level Analysis Failed', 'data': 'Image error level analysis failed due to some error!'})

    except Exception as e:
        return jsonify({'status': False, 'type':'danger', 'message': "Error Exception", 'data': str(e)})

@app.route('/processImageExtraction', methods=['POST'])
def processImageExtraction():
    try:
        if 'image' not in request.files:
            return jsonify({'status': False, 'type':'danger', 'message': 'No Image Selected', 'data': 'No image file provided!'})

        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'status': False, 'type':'danger', 'message': 'Invalid Image', 'data': 'Invalid image file!'})
                
        original_filename = secure_filename(file.filename)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{original_filename}"
        
        file.save(os.path.join(app.config['INPUT_DIR'], filename))
                
        image_extracted = image_extraction.detect(app.config['INPUT_DIR'],app.config['OUTPUT_DIR'], filename)
        
        if image_extracted:
            return jsonify({'status': True, 'type':'success', 'message': 'Image Extracted Successfuly', 'data': 'Image extracted successfuly!', 'image': os.path.join(app.config['OUTPUT_DIR'], filename)})
        else:
            return jsonify({'status': False, 'type':'danger', 'message': 'Image Extraction Failed', 'data': 'Image extraction failed due to some error!'})

    except Exception as e:
        return jsonify({'status': False, 'type':'danger', 'message': "Error Exception", 'data': str(e)})
    
@app.route('/processStringExtraction', methods=['POST'])
def processStringExtraction():
    try:
        if 'image' not in request.files:
            return jsonify({'status': False, 'type':'danger', 'message': 'No Image Selected', 'data': 'No image file provided!'})

        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'status': False, 'type':'danger', 'message': 'Invalid Image', 'data': 'Invalid image file!'})
                
        original_filename = secure_filename(file.filename)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{original_filename}"
        
        file.save(os.path.join(app.config['INPUT_DIR'], filename))
                
        image_string_extraction = string_extraction.detect(app.config['INPUT_DIR'],app.config['OUTPUT_DIR'], filename)
                
        if image_string_extraction:
            return jsonify({'status': True, 'type':'success', 'message': "Image String Extracted", 'data': image_string_extraction})
        else:
            return jsonify({'status': False, 'type':'danger', 'message': 'Image String Extraction Failed', 'data': 'Image string extraction failed due to some error!'})

    except Exception as e:
        return jsonify({'status': False, 'type':'danger', 'message': "Error Exception", 'data': str(e)})
    
@app.route('/processCopyMoveDetection', methods=['POST'])
def processCopyMoveDetection():
    try:
        if 'image' not in request.files:
            return jsonify({'status': False, 'type':'danger', 'message': 'No Image Selected', 'data': 'No image file provided!'})

        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'status': False, 'type':'danger', 'message': 'Invalid Image', 'data': 'Invalid image file!'})
                
        original_filename = secure_filename(file.filename)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{original_filename}"
        
        file.save(os.path.join(app.config['INPUT_DIR'], filename))
                
        image_copy_move_detection = copy_move_detection.detect(app.config['INPUT_DIR'],app.config['OUTPUT_DIR'], filename)
        
        if image_copy_move_detection:
            return jsonify({'status': True, 'type':'danger', 'message': 'Copy Move Forgery Detected', 'data': 'Copy move forgery detected in image!', 'image': os.path.join(app.config['OUTPUT_DIR'], filename)})
        else:
            return jsonify({'status': True, 'type':'success', 'message': 'No Copy Move Detected', 'data': 'No copy move detection found!', 'image': os.path.join(app.config['INPUT_DIR'], filename)})

    except Exception as e:
        return jsonify({'status': False, 'type':'danger', 'message': "Error Exception", 'data': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
