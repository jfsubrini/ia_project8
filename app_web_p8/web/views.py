"""All the views for the web app of the app_web_p8 project.
    """
from django.shortcuts import render


# Semantic Segmentation views.
def semantic_seg_request(request):
    """View to the semantic segmentation request form page."""
    # To display the empty semantic segmentation request form.
    return render(request, "semantic_seg_request.html")

def semantic_seg_response(request):
    """View to the semantic segmentation response page."""
    # To display the semantic segmentation response page from the REST API.
    return render(request, "semantic_seg_response.html")

#############################################################
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

# import requests
# url = "https://frozen-savannah-32709.herokuapp.com/"
# payload={}
# path = 'datasets/images/test/berlin/berlin_000000_000019_leftImg8bit.png'
# files=[('file',(path, open(path,'rb'),'image/png'))]
# headers = {'accept': 'application/json'}
# response = requests.request("POST", url, headers=headers, 
#                             data=payload, files=files)
# print(response.text)
