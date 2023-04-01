# -*- coding: utf-8 -*-
# pylint: disable=unused-argument,no-member,invalid-name,missing-class-docstring
"""The admin page to add, modify and delete images and respective masks.
The page to select an image to send to the REST API.
The page to display the image sent, the respective ground truth mask and the
predicted mask (response from the REST API).
    """

import json
import os
import numpy as np
import requests
from django.contrib import admin
from django.http import HttpResponseRedirect
from PIL import Image as im
from .models import Image


# CUSTOM ADMIN ACTIONS TO MAKE THE SEMANTIC SEGMENTATION REQUEST.
# Web action to make the semantic segmentation request to the REST API,
# sending an image.
@ admin.action(description="Faire une requête à l'API avec une seule image.")
def make_semantic_seg_request(modeladmin, request, queryset):
    """ Admin Action to make a request.
        Sending a selected image to a REST API.
        Getting the predicted mask response of that image.
        Saving this predicted mask into the Image model.
        Displaying the new predicted mask inside the page, near the corresponding ground truth mask.
    """
    # Getting the actual selected image to be sent in the request.
    image_selected = queryset.first().image

    # Sending the selected binary image to the REST API with the files parameter of requests.post().
    if os.environ.get("ENV") == "PRODUCTION":
        URL = "https://ia-api-project8.herokuapp.com/"
    else:
        URL = "http://127.0.0.1:8080/segmentation_map/"
    file = [('file', ('myfile.png', open('./media/' + str(image_selected), 'rb'), 'image/png'))]
    response = requests.post(URL, files=file, timeout=10)

    # Converting the REST API response into JSON format.
    json_resp = response.json()

    # Decoding the json response into a numpy array with shape (256, 512, 3).
    resp_array = np.array(json.loads(json_resp))

    # Transforming the numpy array into a PIL Image.
    msk_pred = im.fromarray(resp_array.astype(np.uint8))

    # Saving the predicted mask into the media/prediction directory.
    image_selected_mask_name = queryset.first().title_msk
    title_pred = image_selected_mask_name + "_pred"
    msk_pred.save(f"./media/prediction/{title_pred}.png")

    # Saving the predicted mask (path) and title into the Image table.
    image_selected_id = queryset.first().id
    img = Image.objects.get(id=image_selected_id)
    img.title_prediction = title_pred
    img.mask_pred = f"prediction/{title_pred}.png"
    img.save(update_fields=['title_prediction', 'mask_pred'])

    # Displaying the new image changing list with the new predicted mask.
    return HttpResponseRedirect('/admin/web/image')

########################################################################
# IMAGE & MASK CRUD.
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("title_img", "image_preview",
                    "mask_preview",
                    "pred_mask_preview")
    ordering = ("title_img",)
    search_fields = ("title_img",)
    readonly_fields = ('image_preview', "mask_preview",
                       "pred_mask_preview")
    actions = (make_semantic_seg_request,)
