from django.shortcuts import render
import requests
import json
import cv2


URL = 'http://localhost:8000/'
# prepare headers for http request.
headers = {'content-type': 'image/png'}
img = cv2.imread('image_test.png')
# encode image as png.
_, img_encoded = cv2.imencode('.png', img)
# send http request with image and receive response.
response = requests.post(URL, data=img_encoded.tostring(), headers=headers)
# decode response.
print(json.loads(response.text))


# def post_image(img_file):
#     """ post image and return the response """
#     img = open(img_file, 'rb').read()
#     response = requests.post(URL, data=img, headers=headers)
#     return response
