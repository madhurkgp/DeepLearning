# Important imports
from app import app
from flask import request, render_template, redirect, url_for
import os
from skimage.metrics import structural_similarity
import imutils
import cv2
import numpy as np
from PIL import Image

# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'

# Route to home page
@app.route("/", methods=["GET", "POST"])
def index():

    # Execute if request is get
    if request.method == "GET":
        return render_template("index.html")

    # Execute if request is post
    if request.method == "POST":
        option = request.form['options']
        image_upload = request.files['image_upload']
        imagename = image_upload.filename
        image = Image.open(image_upload)
        image_logow = np.array(image.convert('RGB'))
        h_image, w_image, _ = image_logow.shape
        
        if option == 'logo_watermark':
            logo_upload = request.files['logo_upload']
            logoname = logo_upload.filename
            logo = Image.open(logo_upload)
            logo = np.array(logo.convert('RGB'))
            h_logo, w_logo, _ = logo.shape
            center_y = int(h_image / 2)
            center_x = int(w_image / 2)
            top_y = center_y - int(h_logo / 2)
            left_x = center_x - int(w_logo / 2)
            bottom_y = top_y + h_logo
            right_x = left_x + w_logo

            roi = image_logow[top_y: bottom_y, left_x: right_x]
            result = cv2.addWeighted(roi, 1, logo, 1, 0)
            cv2.line(image_logow, (0, center_y), (left_x, center_y), (0, 0, 255), 1)
            cv2.line(image_logow, (right_x, center_y), (w_image, center_y), (0, 0, 255), 1)
            image_logow[top_y: bottom_y, left_x: right_x] = result

            img = Image.fromarray(image_logow, 'RGB')
            img.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image.png'))
            full_filename =  'static/uploads/image.png'
            return render_template('index.html', full_filename = full_filename)

        else:
            text_mark = request.form['text_mark']
            if not text_mark:
                text_mark = "Watermark"

            # Calculate text position (bottom right corner)
            font_scale = 1
            thickness = 2
            font = cv2.FONT_HERSHEY_SIMPLEX
            
            # Get text size to position it properly
            (text_width, text_height), baseline = cv2.getTextSize(text_mark, font, font_scale, thickness)
            
            # Position text at bottom right with some padding
            text_x = w_image - text_width - 20
            text_y = h_image - 20
            
            cv2.putText(image_logow, text=text_mark, org=(text_x, text_y), fontFace=font, fontScale=font_scale,
            color=(0,0,255), thickness=thickness, lineType=cv2.LINE_AA) 
            timg = Image.fromarray(image_logow, 'RGB')
            timg.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image1.png'))
            full_filename =  'static/uploads/image1.png'
            return render_template('index.html', full_filename = full_filename)

       
# Main function
if __name__ == '__main__':
    app.run(debug=True)
