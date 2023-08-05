from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CategoriesConfig(AppConfig):
    name = 'myproject.apps.categories'
    verbose_name = _('Categories')

