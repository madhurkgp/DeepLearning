# Important imports
from app import app
from flask import request, render_template, url_for
from keras import models
import numpy as np
from PIL import Image
import string
import random
import os
from keras.preprocessing import image

# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'

# Loading model
model = models.load_model('app/static/model/bird_species.h5')

# Route to home page
@app.route("/", methods=["GET", "POST"])
def index():

	# Execute if request is get
	if request.method == "GET":
		full_filename =  'images/white_bg.jpg'
		return render_template("index.html", full_filename = full_filename)

	# Execute if reuqest is post
	if request.method == "POST":

		# Reading, resizing, saving and preprocessing image for predicition 
		image_upload = request.files['image_upload']
		imagename = image_upload.filename
		
		# Proper preprocessing for the model
		img = image.load_img(image_upload, target_size=(224, 224))
		img_array = image.img_to_array(img)
		img_array = np.expand_dims(img_array, axis=0)
		img_array = img_array / 255.0  # Normalize to [0,1] range
		
		# Generate unique filename and save the resized image for display
		letters = string.ascii_lowercase
		name = ''.join(random.choice(letters) for i in range(10)) + '.png'
		full_filename =  'uploads/' + name
		display_image = Image.fromarray((img_array[0] * 255).astype(np.uint8))
		display_image.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], name))

		# Predicting output
		result = model.predict(img_array)
		ind = np.argmax(result)
		classes = ['AMERICAN GOLDFINCH', 'BARN OWL', 'CARMINE BEE-EATER', 'DOWNY WOODPECKER', 'EMPEROR PENGUIN', 'FLAMINGO']

		# Returning template, filename, extracted text
		return render_template('index.html', full_filename = full_filename, pred = classes[ind])

# Main function
if __name__ == '__main__':
    app.run(debug=True)
