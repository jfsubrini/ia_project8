# -*- coding: utf-8 -*-
# pylint: disable=no-member,import-error
"""
Created by Jean-François Subrini on the 1st of April 2023.
Creation of a semantic segmentation REST API using the FastAPI framework
and a U-NET model (created in the Notebook 1 Scripts).
This REST API has been deployed on Heroku at https://ia-api-project8.herokuapp.com/.
"""
### IMPORTS ###
# Importation of Python modules and methods.
import json
from io import BytesIO
# Importation of libraries.
import cv2
import numpy as np
import uvicorn
from PIL import Image
# import tensorflow as tf
from tensorflow.keras.models import load_model
from fastapi import (
    FastAPI,
    File,
    HTTPException,
    UploadFile,
)


### LOADING MODEL & PREDICTION FUNCTIONS ###
# Loading the selected UNET model.
unet_model = load_model('model_unet_dice_loss_tuning', compile=False)
# Image size.
IMG_HEIGHT = 256
IMG_WIDTH = 512

def get_colored(pred_mask, n_classes):
    """Function to get the prediction mask colored as wanted
    for the different 8 classes."""
    # This color map has been used to display the results in the predicted mask.
    color_map = {
        0: (0, 0, 0),        # void (black)
        1: (160, 120, 50),   # flat (brown)
        2: (255, 200, 200),  # construction (pink)
        3: (255, 255, 120),  # object (yellow)
        4: (0, 150, 40),     # nature (green)
        5: (0, 180, 230),    # sky (sky blue)
        6: (255, 80, 80),    # human (red)
        7: (90, 40, 210)     # vehicule (blue purple)
    }
    mask_height = pred_mask.shape[0]
    mask_width = pred_mask.shape[1]
    pred_mask_c = np.zeros((mask_height, mask_width, 3))

    for cls in range(n_classes):
        pred_mask_rgb = pred_mask[:, :] == cls
        pred_mask_c[:, :, 0] += ((pred_mask_rgb) * (color_map[cls][0])).astype('uint8') # R
        pred_mask_c[:, :, 1] += ((pred_mask_rgb) * (color_map[cls][1])).astype('uint8') # G
        pred_mask_c[:, :, 2] += ((pred_mask_rgb) * (color_map[cls][2])).astype('uint8') # B

    return pred_mask_c.astype('uint8')

def mask_prediction(model, img_to_predict):
    """Function that makes, with a model, the mask prediction of an image.
    """
    img_resized = cv2.resize(img_to_predict, (IMG_WIDTH, IMG_HEIGHT))
    pred_mask = model.predict(np.expand_dims(img_resized, axis=0))
    pred_mask = np.argmax(pred_mask, axis=-1)
    pred_mask = np.expand_dims(pred_mask, axis=-1)
    pred_mask = np.squeeze(pred_mask)
    pred_mask_colored = get_colored(pred_mask, 8)

    return pred_mask_colored

def load_img_into_np_array(img):
    """Reading the bytes file sent by the client (Django website) and transform it
    into numpy array."""
    return np.array(Image.open(BytesIO(img)))


### FASTAPI INSTANCE FOR IMAGE SEMANTIC SEGMENTATION ###
# Creating the app object.
app = FastAPI()

# Index route, opens automatically on http://127.0.0.1:8000.
# after typing 'uvicorn main:app --reload' in the Terminal.
# or http://127.0.0.1:8080 with 'uvicorn main:app --reload --port 8080' if Django client.
@app.get('/')
def index():
    """Welcome message"""
    return {'message': 'This is a semantic segmentation app.'}

# Route to access to the FastAPI swagger, at: http://127.0.0.1:8000/docs,
# or at: http://127.0.0.1:8000/segmentation_map to upload directly the image
# to generate the respective predictive mask, in json form.
@app.post('/segmentation_map')
async def get_segmentation_map(file : UploadFile = File(...)):
    """Get segmentation maps from image file."""
    try:
        # Reading the image sent by the client (Django website).
        image_from_client = await file.read()
        # Preparing the image for prediction.
        img_to_predict = load_img_into_np_array(image_from_client) / 255.0
        # Predicting the mask.
        pred_mask_colored = mask_prediction(unet_model, img_to_predict)
        # Returning the mask as a json string.
        return json.dumps(pred_mask_colored.tolist())

    except HTTPException:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

# Running the API with uvicorn.
# Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    