from flask import Flask, request, jsonify
from helpers import perform_reverse_search
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static'

@app.route('/')
def home():
    return "Image Search Backend is Running!"

@app.route('/reverse-search', methods=['POST'])
def reverse_search():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(file_path)

    # Perform reverse image search
    results = perform_reverse_search(file_path)

    # Clean up
    os.remove(file_path)

    return jsonify({'results': results}), 200

if __name__ == '__main__':
    app.run(debug=True)
