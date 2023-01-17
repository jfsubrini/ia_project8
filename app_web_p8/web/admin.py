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
# from django.http import HttpResponseRedirect
from .models import Image


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
    # Sending the request to the REST API with the selected image.
    # You can directly post binary image to the server using the files parameter of requests.post():
    # URL = "https://ia-api-project8.herokuapp.com/"
    URL = "http://127.0.0.1:8080/segmentation_map/"
    with open('./media/' + str(image_selected), 'rb') as file_handle:
    # my_img = {'file': open('./media/' + str(image_selected), 'rb')}
        my_img = {'file': file_handle}
        response = requests.post(URL, files=my_img, timeout=10)
    # # convert server response into JSON format.

    # # Getting the response of the REST API : the predicted mask of the selected image sent.

    # Saving the predicted mask into the Image table, related to the right image, and its title.
    image_selected_mask_name = queryset.first().title_msk
    title_pred = image_selected_mask_name + "_pred"
    image_selected_id = queryset.first().id
    img = Image.objects.get(id=image_selected_id)
    img.title_prediction = title_pred
    # Decoding the json response.
    json_resp = json.loads(response)
    print(json_resp)
    # img.mask_pred = json_resp
    # img.save(update_fields=['mask_pred', 'title_prediction'])

    # # Displaying the new image changing list with the new predicted mask.
    # return HttpResponseRedirect('/admin')

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


########################################################################
#         orderline_list = request.POST.getlist('_selected_action')
#         # Put the new bill id created in the invoiced order line(s) instance(s).
#         for orderline in orderline_list:
#             orderline_selected = OrderLine.objects.filter(
#                 id=orderline).last()
#             bill_id = Bill.objects.filter(id=new_bill.id).last()
#             orderline_selected.bill_id = bill_id
#             orderline_selected.save()

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

# return Response(img, mimetype="image/png")
