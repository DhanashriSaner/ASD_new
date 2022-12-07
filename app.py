from flask import Flask, render_template, request

import numpy as np
import os

from keras_preprocessing.image import load_img
from keras_preprocessing.image import img_to_array
from keras.models import load_model

#load model
model =load_model("model/best_model.h5")

print('@@ Model loaded')


def pred_ASD(cott_plant):
  test_image = load_img(cott_plant, target_size = (150, 150)) # load image 
  print("@@ Got Image for prediction")
  
  test_image = img_to_array(test_image)/255 # convert image to np array and normalize
  test_image = np.expand_dims(test_image, axis = 0) # change dimention 3D to 4D
  
  result = model.predict(test_image).round(3) # predict diseased plant or not
  print('@@ Raw result = ', result)
  
  pred = np.argmax(result) # get the index of max value

  if pred == 0:
    return 'You Are Suffering with Autism Spectrum Disorder'      

  else:
    return 'Healthy' # if index 3

#------------>>pred_cot_dieas<<--end
    

# Create flask instance
app = Flask(__name__)

# render index.html page
@app.route("/", methods=['GET', 'POST'])
def home():
        return render_template('index.html')
    
 
# get input image from client then predict class and render respective .html page for solution
@app.route("/predict", methods = ['GET','POST'])
def predict():
     if request.method == 'POST':
        file = request.files['file'] # fet input
        filename = file.filename        
        print("@@ Input posted = ", filename)
        
        file_path = os.path.join('static/uploads', filename)
        file.save(file_path)

        print("@@ Predicting class......")
        pred, output_page = pred_ASD(cott_plant=file_path)
              
        return render_template(output_page, pred_output = pred, user_image = file_path)
    
# For local system & cloud
if __name__ == "__main__":
    app.run(threaded=False,) 
    
    