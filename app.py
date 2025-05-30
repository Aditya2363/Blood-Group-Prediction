import cv2
import numpy as np
import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to analyze image histogram
def analyze_histogram(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Convert to grayscale
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])  # Histogram of intensities
    return hist.flatten()

# Function to detect edges in the image
def detect_edges(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(image, 50, 150)  # Apply Canny Edge Detection
    edge_count = np.sum(edges > 0)  # Count the number of edge pixels
    return edge_count

# Function to predict blood group based on image features
def predict_blood_group(hist, edge_count):
    mean_intensity = np.mean(hist)
    
    if mean_intensity > 100 and edge_count > 5000:
        return "A"
    elif mean_intensity > 120 and edge_count < 5000:
        return "B"
    elif mean_intensity < 100 and edge_count > 4000:
        return "AB"
    else:
        return "O"

@app.route('/')
def upload_form():
    return render_template('index.html')
    
@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload.html', result="No file selected.")

        file = request.files['file']
        
        if file.filename == '':
            return render_template('upload.html', result="No file selected.")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            hist = analyze_histogram(filepath)
            edge_count = detect_edges(filepath)
            blood_group = predict_blood_group(hist, edge_count)

            return render_template('upload.html', result=f'Predicted Blood Group: {blood_group}', image_path=filepath)
        else:
            return render_template('upload.html', result="Invalid file type. Please upload a PNG or JPG image.")
    else:
        return render_template('upload.html')

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
