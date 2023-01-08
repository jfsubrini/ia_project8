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

    title_img = models.CharField(
        "Titre de l'image", max_length=50, unique=True)
    image = models.ImageField(upload_to='images')
    title_msk = models.CharField(
        "Titre du mask", max_length=50, unique=True )
    mask = models.ImageField(upload_to='masks')
    title_prediction = models.CharField(
        "Titre de la prédiction", max_length=50, 
        unique=True, blank=True, null=True)
    mask_pred = models.ImageField(
        upload_to='prediction', blank=True, null=True)
    
    def image_preview(self):
        """Displaying the image, size 180x360."""
        return mark_safe(f'<img src="{self.image.url}" width="360" height="180"/>')

    def mask_preview(self):
        """Displaying the mask, size 180x360."""
        return mark_safe(f'<img src="{self.mask.url}" width="360" height="180"/>')

    def pred_mask_preview(self):
        """Displaying the predicted mask, size 180x360."""
        if self.mask_pred:
            return mark_safe(f'<img src="{self.mask_pred.url}" width="360" height="180"/>')
        return None
    
    class Meta:
        verbose_name = "Image & Mask storing"

    def __str__(self):
        return f"Image {self.title_img} et Mask {self.title_msk}"
