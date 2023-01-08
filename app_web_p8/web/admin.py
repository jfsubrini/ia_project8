# -*- coding: utf-8 -*-
# pylint: disable=missing-class-docstring, no-member
"""The admin page to add, modify and delete images and respective masks.
The page to select an image to send to the REST API.
The page to display the image sent, the respective ground truth mask and the 
predicted mask (response from the REST API).
    """
from django.contrib import admin
from .models import Image

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    # exclude = ("title_msk", "mask")
    list_display = ("title_img", "image_preview", 
                    "title_msk", "mask_preview")
    ordering = ("title_img",)
    search_fields = ("title_img",)
    readonly_fields = ('image_preview', "mask_preview")

# from django.shortcuts import render
# import requests
# import json
# import cv2


# URL = 'http://localhost:8000/'
# # prepare headers for http request.
# headers = {'content-type': 'image/png'}
# img = cv2.imread('image_test.png')
# # encode image as png.
# _, img_encoded = cv2.imencode('.png', img)
# # send http request with image and receive response.
# response = requests.post(URL, data=img_encoded.tostring(), headers=headers)
# # decode response.
# print(json.loads(response.text))


# # def post_image(img_file):
# #     """ post image and return the response """
# #     img = open(img_file, 'rb').read()
# #     response = requests.post(URL, data=img, headers=headers)
# #     return response
