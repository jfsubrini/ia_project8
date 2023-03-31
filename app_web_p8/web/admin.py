# -*- coding: utf-8 -*-
# pylint: disable=unused-argument,no-member,invalid-name,missing-class-docstring
"""The admin page to add, modify and delete images and respective masks.
The page to select an image to send to the REST API.
The page to display the image sent, the respective ground truth mask and the
predicted mask (response from the REST API).
    """

import json
import requests
from django.contrib import admin
from django.http import HttpResponseRedirect
from .models import Image
from PIL import Image as im
import numpy as np
import cv2
from django.core.files.base import ContentFile


# CUSTOM ADMIN ACTIONS TO MAKE THE SEMANTIC SEGMENTATION REQUEST.
# Web action to make the semantic segmentation request to the REST API,
# sending an image.
@ admin.action(description="Faire une requête à l'API avec une seule image.")
def make_semantic_seg_request(modeladmin, request, queryset):
    """ Admin Action to make a request.
        Sending a selected image to a REST API.
        Getting the predicted mask response of that image.
        Saving this mask into the Image model.
    """
    # Getting the actual selected image to be sent in the request.
    image_selected = queryset.first().image
    # print("image_selected ", image_selected)
    # print(str(image_selected).removeprefix('image/'))
    # Sending the request to the REST API with the selected image.
    # You can directly post binary image to the server using the files parameter of requests.post():
    # URL = "https://ia-api-project8.herokuapp.com/"
    URL = "http://127.0.0.1:8080/segmentation_map/"
    # with open('./media/' + str(image_selected), 'rb') as file_handle:
    file = [('file', ('myfile.png', open('./media/' + str(image_selected), 'rb'), 'image/png'))]
    response = requests.post(URL, files=file, timeout=10)
    # # convert server response into JSON format.
    # resp = response.json()
    # # Getting the response of the REST API : the predicted mask of the selected image sent.

    # Saving the predicted mask into the Image table, related to the right image, and its title.
    image_selected_mask_name = queryset.first().title_msk
    title_pred = image_selected_mask_name + "_pred"
    image_selected_id = queryset.first().id
    img = Image.objects.get(id=image_selected_id)
    img.title_prediction = title_pred
    # Decoding the json response.
    # json_resp = response.json()
    json_resp = json.loads(response.json())
    resp_array = np.array(json_resp)
    img_gg = im.fromarray(resp_array.astype(np.uint8))
    img_gg.show()
    img.mask_pred = img_gg
    img.save(update_fields=['mask_pred', 'title_prediction'])  # TODO

    # Displaying the new image changing list with the new predicted mask.
    return HttpResponseRedirect('/admin')

########################################################################
# IMAGE & MASK CRUD
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("title_img", "image_preview",
                    "title_msk", "mask_preview",
                    "title_prediction", "pred_mask_preview")
    ordering = ("title_img",)
    search_fields = ("title_img",)
    readonly_fields = ('image_preview', "mask_preview",
                       "pred_mask_preview")
    actions = (make_semantic_seg_request,)
