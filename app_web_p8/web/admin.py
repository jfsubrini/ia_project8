# -*- coding: utf-8 -*-
# pylint: disable=missing-class-docstring, no-member
"""The admin page to add, modify and delete images and respective masks.
The page to select an image to send to the REST API.
The page to display the image sent, the respective ground truth mask and the 
predicted mask (response from the REST API).
    """
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
        Saving this mask into the Image model."""
    pass
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


# CUSTOM ADMIN ACTIONS TO CREATE INITIAL AND FINAL STOCKS INVENTORIES.
# Initial Bar Stock inventory action from the Bar list page.
# @admin.action(description='Inventaire du stock initial du bar')
# def make_bar_initial_stocks(modeladmin, request, queryset):
#     """ Action pour faire un inventaire du stock initial du bar ; \
#         envoi vers une page intermédiaire ; enregistrement des données \
#         dans la table de Stock."""
#     if "apply" in request.POST:
#         # Saving the data from the initial bar stock inventory form
#         # to update the Stock table with those data.
#         drinks_list = request.POST.getlist('_selected_action')
#         drink_quantity_list = request.POST.getlist('drink_quantity')
#         trip_selected = request.POST['trip']
#         trip_id_selected = Trip.objects.filter(id=trip_selected).last()
#         i = 0
#         for drink in drinks_list:
#             if drink_quantity_list[i]:
#                 drink_quantity = drink_quantity_list[i]
#             else:
#                 drink_quantity = 0
#             i = i + 1
#             if drink_quantity != 0:
#                 drink_id_selected = Bar.objects.filter(id=drink).last()
#                 bar_initial_item = Stock(bar_initial_id=drink_id_selected,
#                                          trip_id=trip_id_selected, quantity=drink_quantity,
#                                          user_id=request.user)
#                 bar_initial_item.save()
#         return HttpResponseRedirect('/admin')

#     # To display the stock inventory with all the drinks registered into the database
#     # with the choice of trips.
#     else:
#         all_drinks = queryset.all()
#         all_trips = Trip.objects.all()

#     # What to render to the template.
#     all_drinks = queryset.all()
#     all_trips = Trip.objects.all()
#     return render(request, 'admin/bar_initial_stocks.html',
#                   context={"drinks": all_drinks, "trips": all_trips})


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
