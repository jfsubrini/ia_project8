# -*- coding: utf-8 -*-
"""
Created by Jean-François Subrini on the 12th of January 2023.
Creation of a semantic segmentation REST API using the FastAPI framework
and a U-NET model (created in the Notebook 1 Scripts).
This REST API has been deployed on Heroku at https://ia-api-project8.herokuapp.com/.
"""
### IMPORTS ###
# Importation of Python modules and methods.
# import json
import jsonpickle
# import io

# Importation of libraries.
import cv2
import numpy as np
import uvicorn
# import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import img_to_array
from fastapi import (
    FastAPI,
    File,
    HTTPException,
    Response,
    UploadFile,
)
# from fastapi.responses import JSONResponse
# from fastapi.encoders import jsonable_encoder
# from PIL import Image

### LOADING MODEL & FASTAPI INSTANCE ###
# Loading the selected UNET model.
selected_model = load_model('model3_unet_vgg16', compile=False)

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
    """Function that make the mask prediction with an image.
    Printing of the image, the ground truth mask and the colored prediction mask."""

    print("MODEL ", model)
    print("img_to_predict ", img_to_predict)
    img_resized = cv2.resize(img_to_predict, (IMG_WIDTH, IMG_HEIGHT))
    print("ICICIICICICICICICIC", img_resized)
    pred_mask = model.predict(np.expand_dims(img_resized, axis=0))
    pred_mask = np.argmax(pred_mask, axis=-1)
    pred_mask = np.expand_dims(pred_mask, axis=-1)
    pred_mask = np.squeeze(pred_mask)
    pred_mask_colored = get_colored(pred_mask, 8)

    return pred_mask_colored

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
    """Get segmentation maps from image file."""    
    try:
        img_to_predict = file.file.read()
        with open(file.filename, 'wb') as f:
            print("FFFFFFFFFfopen ", f)
            f.write(img_to_predict)
            # Predicting the segmentation map (mask).
            to_predict = img_to_array(f) / 255.0
            print("to_predict ", to_predict)
            pred_mask_colored = mask_prediction(selected_model, to_predict)
            print("RETURN ", pred_mask_colored)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    return {"message": f"Successfuly uploaded {file.filename}"}
    
    
#     if file.filename.endswith(".png"):
#         print("LALALALLALALALLALALAL ", file)
#     # Read the image sent by the client (Django website).
#         img_to_predict = await file.read()
#         print("LA ", img_to_predict)
#         # img_to_predict = img_to_array(load_img(image_train_paths[i])) / 255.0
#         # Predicting the segmentation map (mask).
#         pred_mask_colored = mask_prediction(selected_model, img_to_predict)
#         # Encoding the response using jsonpickle.
#         response_pickled = jsonpickle.encode(pred_mask_colored)

# #         response_pickled = jsonpickle.encode(file)  # OU BIEN CELUI-LA

# #         return Response(content=image_bytes, media_type='application/json')  # OU BIEN CA

# #         result = {'meta': {'status': 200}, 'data': file}
# #         content = jsonable_encoder(result)
# #         return JSONResponse(content=content)  # OU BIEN CA

#         return Response(content=response_pickled, media_type='application/json')
#     raise HTTPException(
#         400, detail="Invalid file or format type (needs .png image)")

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


#         image = Image.open(io.BytesIO(image_bytes))
        # Read the bytes file sent by the client (Django website) and transform it into an image.
    #     image = Image.open(io.BytesIO(file))
#         image.show()
#         return Response(response=response_pickled, status=200, mimetype="application/json")

# Running the API with uvicorn.
# Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    