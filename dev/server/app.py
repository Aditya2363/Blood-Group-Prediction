from flask import Flask, request, jsonify
import cv2
import numpy as np
import tensorflow as tf
import os

app = Flask(__name__)

# Load the trained ML model
model = tf.keras.models.load_model("blood_group_model.h5")

# Blood group labels
labels = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

@app.route("/detect", methods=["POST"])
def detect_blood_group():
    file = request.files["file"]
    file_path = "uploads/" + file.filename
    file.save(file_path)

    # Load and preprocess the image
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (128, 128))  
    image = np.expand_dims(image, axis=-1)  
    image = np.expand_dims(image, axis=0)  

    # Make prediction
    prediction = model.predict(image)
    blood_group = labels[np.argmax(prediction)]

    os.remove(file_path)  

    return jsonify({"blood_group": blood_group})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
