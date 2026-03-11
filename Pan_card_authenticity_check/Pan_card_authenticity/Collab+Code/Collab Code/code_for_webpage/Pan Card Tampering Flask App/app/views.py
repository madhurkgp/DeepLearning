# Important imports
from app import app
from flask import request, render_template, url_for
import os
from skimage.metrics import structural_similarity
import imutils
import cv2
from PIL import Image
import numpy as np

# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'
app.config['EXISTNG_FILE'] = 'app/static/original'
app.config['GENERATED_FILE'] = 'app/static/generated'

# Ensure directories exist
os.makedirs(app.config['INITIAL_FILE_UPLOADS'], exist_ok=True)
os.makedirs(app.config['EXISTNG_FILE'], exist_ok=True)
os.makedirs(app.config['GENERATED_FILE'], exist_ok=True)

# Route to home page
@app.route("/", methods=["GET", "POST"])
def index():
    # Execute if request is get
    if request.method == "GET":
        return render_template("index.html")

    # Execute if request is post
    if request.method == "POST":
        try:
            # Get uploaded image
            file_upload = request.files['file_upload']
            filename = file_upload.filename
            
            if not filename:
                return render_template("index.html", error="No file selected")

            # Resize and save the uploaded image
            uploaded_image = Image.open(file_upload).resize((250,160))
            uploaded_image.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image.jpg'))

            # Resize and save the original image to ensure both uploaded and original matches in size
            # Check if original image exists, if not handle it (though in this specific app logic it seems hardcoded)
            original_path = os.path.join(app.config['EXISTNG_FILE'], 'image.jpg')
            if not os.path.exists(original_path):
                 return render_template("index.html", error="Original reference image missing on server")

            original_image = Image.open(original_path).resize((250,160))
            original_image.save(os.path.join(app.config['EXISTNG_FILE'], 'image.jpg'))

            # Read uploaded and original image as array
            original_image = cv2.imread(os.path.join(app.config['EXISTNG_FILE'], 'image.jpg'))
            uploaded_image = cv2.imread(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image.jpg'))

            # Convert image into grayscale
            original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
            uploaded_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)

            # Calculate structural similarity
            (score, diff) = structural_similarity(original_gray, uploaded_gray, full=True)
            diff = (diff * 255).astype("uint8")

            # Calculate threshold and contours
            thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            
            # Draw contours on image
            for c in cnts:
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.rectangle(uploaded_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Save all output images (if required)
            cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_original.jpg'), original_image)
            cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_uploaded.jpg'), uploaded_image)
            cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_diff.jpg'), diff)
            cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_thresh.jpg'), thresh)
            
            return render_template('index.html', pred=str(round(score*100,2)) + '%')
            
        except Exception as e:
            return render_template("index.html", error=f"An error occurred: {str(e)}")

# Main function
if __name__ == '__main__':
    app.run(debug=True)
