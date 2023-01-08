"""Overinding the default Admin with custom P8 header, site title and index title.
    """
from django.contrib.admin import AdminSite


class P8Admin(AdminSite):
    """P8 header, site title and index title."""
    site_header = 'Projet 8 | Administration'
    site_title = 'Projet 8 | Site Admin'
    index_title = "Participez à la conception d'une voiture autonome - \
        Projet 8 | Admin Home"
    