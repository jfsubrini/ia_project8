# -*- coding: utf-8 -*-
"""
Created by Jean-François Subrini on the 12th of January 2023.
Creation of a semantic segmentation REST API using the FastAPI framework 
and a U-NET model (created in the Notebook 1 Scripts).
This REST API has been deployed on Heroku.
"""
### IMPORTS ###
# Importation of Python modules and methods.
import json

# Importation of libraries.
import uvicorn
from fastapi import FastAPI, File, UploadFile
import tensorflow as tf
from tensorflow.keras.models import load_model


### LOADING MODEL & FASTAPI INSTANCE ###
# Loading the selected UNET model.
unet_model = load_model('model_unet')

# Creating the app object.
app = FastAPI()

# # Index route, opens automatically on http://127.0.0.1:8000.
# @app.get('/')
# def index():
#     """Welcome message"""
#     return {'message': 'This is a semantic segmentation app.'}

# Route to access to the FastAPI swagger, at: http://127.0.0.1:8000/docs,
# to upload directly the image to generate the respective predictive mask, 
# in json form.
@app.post('/')
async def get_segmentation_map(file: UploadFile = File(...)):
    """Get segmentation maps from image file."""
    extension = file.filename.split(".")[-1] in ("png")
    if not extension:
        return "Image must be png format!"
    # Predicting the segmentation map (mask).
    image_bytes = await file.read()
    image = tf.io.decode_image(image_bytes)
    prediction = unet_model.predict(tf.expand_dims(image, axis=0))
    return {"prediction": json.dumps(prediction.tolist())}


# Running the API with uvicorn.
# Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

# import requests
# url = "https://frozen-savannah-32709.herokuapp.com/"
# payload={}
# path = 'datasets/images/test/berlin/berlin_000000_000019_leftImg8bit.png'
# files=[('file',(path, open(path,'rb'),'image/png'))]
# headers = {'accept': 'application/json'}
# response = requests.request("POST", url, headers=headers, 
#                             data=payload, files=files)
# print(response.text)
    