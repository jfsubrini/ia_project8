# -*- coding: utf-8 -*-
# pylint: disable=missing-class-docstring, no-member
"""All the admin pages to.....
    """
from django.contrib import admin
from .models import Image


@admin.register(Image)
class WebAdmin(admin.ModelAdmin):
    # exclude = ("image",)
    # list_display = ("title",)
    list_display = ["title", "image"]
