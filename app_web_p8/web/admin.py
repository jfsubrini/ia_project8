# -*- coding: utf-8 -*-
# pylint: disable=missing-class-docstring, no-member
"""The admin page to add, modify and delete images and respective masks.
The page to select an image to send to the REST API.
The page to display the image sent, the respective ground truth mask and the 
predicted mask (response from the REST API).
    """

import requests
from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponseRedirect
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
    # Getting the id of the selected image in the changing list (or the first one if many).
    # image_selected_id = request.POST.getlist('_selected_action')[0]
    # print(image_selected_id)
    # Getting the actual selected image to be sent in the request.
    image_selected_path = queryset.first().image
    print(image_selected_path)
    # Sending the request to the REST API with the selected image.
    # URL = "https://ia-project8.herokuapp.com/"
    # payload={}
    # path = image_selected
    # files=[('file', (path, open(path,'rb'), 'image/png'))]
    # headers = {'accept': 'application/json'}
    # # Getting the response of the REST API : the predicted mask of the selected image sent.
    # response = requests.request("POST", URL, headers=headers, 
    #                                 data=payload, files=files)
    # # Saving the predicted mask into the Image table, related to the right image.
    # image_selected_id = Image(title_img=image_selected.title_img)            
    # mask_pred = Image(mask_pred=response)
    # mask_pred.save()
    # # Displaying the new image changing list with the new predicted mask.
    # return HttpResponseRedirect('/admin')

########################################################################
# IMAGE & MASK CRUD
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("title_img", "image_preview", 
                    "title_msk", "mask_preview")
    ordering = ("title_img",)
    search_fields = ("title_img",)
    readonly_fields = ('image_preview', "mask_preview")
    actions = (make_semantic_seg_request,)


########################################################################
#     # Post the invoiced order line(s).
#     # if request.method == "POST":
#     if 0 == 0:  # request.method == "POST"
#         # if request.POST.get('post'):  TODO
#         # Create the bill instance with the total amount to pay and the user_id
#         new_bill = Bill(user_id=request.user, amount=total_amount)
#         new_bill.save()
#         # Send the bill to the guest's email address.
#         emailto = queryset.first().guest_id.email
#         guest_name = f"{queryset.first().guest_id.first_name} {queryset.first().guest_id.last_name}"
#         formatted_total_amount = f"{total_amount:.2f}"
#         send_email(emailto, guest_name, formatted_total_amount)
#         # send_email(["lea@vaiatea-liveaboard.com", "william@dragondivekomodo.com"])
#         # Collecting all the guest's order line(s) selected.
#         orderline_list = request.POST.getlist('_selected_action')
#         # Put the new bill id created in the invoiced order line(s) instance(s).
#         for orderline in orderline_list:
#             orderline_selected = OrderLine.objects.filter(
#                 id=orderline).last()
#             bill_id = Bill.objects.filter(id=new_bill.id).last()
#             orderline_selected.bill_id = bill_id
#             orderline_selected.save()
#         return HttpResponseRedirect('/admin')

#     # What to render to the intermediate django admin/bill action template.
#     zipped_data = zip(all_orderlines, all_amounts)
#     email_selected = all_orderlines[0].guest_id.email
#     context = {"orderlines": all_orderlines,
#                "zipped_data": zipped_data,
#                "total_amount": total_amount,
#                "email": email_selected}

#     return render(request, 'admin/bill.html', context)
