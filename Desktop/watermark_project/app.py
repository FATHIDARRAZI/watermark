from flask import Flask, render_template, request, redirect, url_for, jsonify
from PIL import Image, ImageEnhance
import os
from watermark import add_watermark, add_text_watermark

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['OUTPUT_FOLDER'] = 'output/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['OUTPUT_FOLDER']):
    os.makedirs(app.config['OUTPUT_FOLDER'])

if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up logging
import logging
from logging.handlers import RotatingFileHandler
handler = RotatingFileHandler('logs/app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        images = request.files.getlist('images')
        watermark_type = request.form['watermark_type']
        opacity = float(request.form['opacity'])
        scale_factor = float(request.form['scale_factor'])
        image_urls = []

        if watermark_type == 'text':
            text = request.form['text']
            for image in images:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"watermarked_{image.filename}")
                image.save(image_path)
                
                add_text_watermark(image_path, output_path, text, opacity, scale_factor, watermark_type)
                
                image_urls.append(url_for('static', filename=f'output/{os.path.basename(output_path)}'))
                
                os.remove(image_path)
        else:
            watermark = request.files['watermark']
            watermark_path = os.path.join(app.config['UPLOAD_FOLDER'], watermark.filename)
            watermark.save(watermark_path)

            for image in images:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"watermarked_{image.filename}")
                image.save(image_path)
                
                add_watermark(image_path, watermark_path, output_path, opacity, scale_factor, watermark_type)
                
                image_urls.append(url_for('static', filename=f'output/{os.path.basename(output_path)}'))
                
                os.remove(image_path)
            
            os.remove(watermark_path)
        
        app.logger.info('Files uploaded and processed successfully')
        return jsonify(success=True, image_urls=image_urls)
    except Exception as e:
        app.logger.error('Failed to upload and process files: %s', e)
        return jsonify(success=False, error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
