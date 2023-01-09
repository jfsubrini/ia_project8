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
import io

# Importation of libraries.
import cv2
import numpy as np
import uvicorn
import tensorflow as tf
from tensorflow.keras.models import load_model
from fastapi import (
    FastAPI, 
    File, 
    HTTPException, 
    Response, 
    UploadFile, 
)
from PIL import Image

### LOADING MODEL & FASTAPI INSTANCE ###
# Loading the selected UNET model.
# unet_model = load_model('model_unet')

# Creating the app object.
app = FastAPI()

# Index route, opens automatically on http://127.0.0.1:8000.
# after typing 'uvicorn main:app --reload' in the Terminal.
@app.get('/')
def index():
    """Welcome message"""
    return {'message': 'This is a semantic segmentation app.'}

# Route to access to the FastAPI swagger, at: http://127.0.0.1:8000/docs,
# or at: http://127.0.0.1:8000/segmentation_map to upload directly the image 
# to generate the respective predictive mask, in json form.
@app.post('/segmentation_map')
async def get_segmentation_map(file : UploadFile = File(...)):
# async def get_segmentation_map(file : bytes=File(...)):
# async def get_segmentation_map(request):
    """Get segmentation maps from image file."""
    if file.filename.endswith(".png"):
    # Read the image sent by the client (Django website).
        image_bytes = await file.read()
    #     response_pickled = jsonpickle.encode(image_bytes)
        image = Image.open(io.BytesIO(image_bytes))
    #     return Response(response=response_pickled, status=200, mimetype="application/json")
        # Read the bytes file sent by the client (Django website) and transform it into an image.
    #     image = Image.open(io.BytesIO(file))
        image.show()
    #     response_pickled = jsonpickle.encode(file)
        response = {"file_name": file.filename}
        return response
    else:
        raise HTTPException(
            400, detail="Invalid file or format type (needs .png image)")
    
#     return Response(response=response_pickled, status=200, mimetype="application/json")
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
    