# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods,missing-class-docstring
"""All the models for the schedule app of the pos_vaiatea project.
    Models: Guest and Trip.
    """
from django.conf import settings
from django.db import models


class Mask(models.Model):
    """
    To create the Mask table in the database.
    Gathering some masks (related to the stored images) of the Cityscapes Dataset.
    """

    title = models.CharField(max_length=50)
    mask = models.ImageField(upload_to='masks')

    class Meta:
        verbose_name = "Mask"

    def __str__(self):
        return f"Mask {self.title}"


class Image(models.Model):
    """
    To create the Image table in the database.
    Gathering some images of the Cityscapes Dataset.
    """

    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images')
    mask = models.OneToOneField(Mask, on_delete=models.CASCADE, 
                                primary_key=True, verbose_name="Mask correspondant")
    
    class Meta:
        verbose_name = "Image"

    def __str__(self):
        return f"Image {self.title}"
