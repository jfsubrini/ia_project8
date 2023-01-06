# -*- coding: utf-8 -*-
# pylint: disable=missing-class-docstring
"""Configuration file for the class and setting of the default_site attributer of the admin app.
    """
from django.contrib.admin.apps import AdminConfig


class P8AdminConfig(AdminConfig):
    default_site = 'app_web_p8.admin.P8Admin'
