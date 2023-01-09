# -*- coding: utf-8 -*-
"""
Created by Jean-François Subrini on the 12th of January 2023.
Creation of a semantic segmentation REST API using the FastAPI framework 
and a U-NET model (created in the Notebook 1 Scripts).
This REST API has been deployed on Heroku at https://ia-api-project8.herokuapp.com/.
"""
### IMPORTS ###
# Importation of Python modules and methods.
import json
import jsonpickle

# Importation of libraries.
import cv2
import numpy as np
import uvicorn
from fastapi import FastAPI, File, UploadFile
import tensorflow as tf
from tensorflow.keras.models import load_model


### LOADING MODEL & FASTAPI INSTANCE ###
# Loading the selected UNET model.
# unet_model = load_model('model_unet')

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
# async def get_segmentation_map(file: UploadFile = File(...)):
async def get_segmentation_map(request: Request):
    """Get segmentation maps from image file."""
    # Read the image sent by the client (Django website).
#     image_bytes = await request.read()
#     response_pickled = jsonpickle.encode(image_bytes)
#     return Response(response=response_pickled, status=200, mimetype="application/json")   
      return Response(response={"name": request.filename})   

#     # Predicting the segmentation map (mask).
#     image = tf.io.decode_image(image_bytes)
#     prediction = unet_model.predict(tf.expand_dims(image, axis=0))
#     return {"prediction": json.dumps(prediction.tolist())}
#     client_host = request.client.host
#     # convert string of image data to uint8
#     nparr = np.fromstring(r.data, np.uint8)
#     # decode image
#     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

# Building a response dictionary to send back to client.
#     response = {'message': image_bytes}
#     # encode response using jsonpickle
#     response_pickled = jsonpickle.encode(response)
#     return Response(response=response_pickled, status=200, mimetype="application/json")
#     return Response(response=response, status=200, mimetype="application/json")


# Running the API with uvicorn.
# Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    