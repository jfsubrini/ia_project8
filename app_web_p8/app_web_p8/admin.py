"""Overinding the default Admin with custom P8 header, site title and index title.
    """
from django.contrib.admin import AdminSite


class P8Admin(AdminSite):
    """P8 header, site title and index title."""
    site_header = 'P8 Administration'
    site_title = 'P8 Site Admin'
    index_title = 'P8 Site Admin Home'