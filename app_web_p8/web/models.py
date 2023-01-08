# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods,missing-class-docstring
"""The Image model to store images and respective mask.
"""
from django.conf import settings
from django.db import models
from django.utils.html import mark_safe


class Image(models.Model):
    """
    To create the Image table in the database.
    Gathering some images and the related mask of the Cityscapes Dataset.
    """

    title_img = models.CharField("Titre de l'image", max_length=50)
    image = models.ImageField(upload_to='images')
    title_msk = models.CharField("Titre du mask", max_length=50)
    mask = models.ImageField(upload_to='masks')
    
    def image_preview(self):
        """Displaying the image, size 180x360."""
        return mark_safe(f'<img src="{self.image.url}" width="360" height="180"/>')

    def mask_preview(self):
        """Displaying the mask, size 180x360."""
        return mark_safe(f'<img src="{self.mask.url}" width="360" height="180"/>')
       
    class Meta:
        verbose_name = "Image & Mask storing"

    def __str__(self):
        return f"Image {self.title_img} et Mask {self.title_msk}"
