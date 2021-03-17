from django.contrib import admin
from .models import Car, NewUser, BookedCars
# Register your models here.
admin.site.register(Car)
admin.site.register(NewUser)
admin.site.register(BookedCars)
