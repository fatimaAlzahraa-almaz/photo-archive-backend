from django.contrib import admin

from .models import Menus
from .models import MenuCategory
from .models import Reservation


# Register your models here.
#from models.py import Drinks

admin.site.register(Menus)
admin.site.register(MenuCategory)
admin.site.register(Reservation)
