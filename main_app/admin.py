from django.contrib import admin

# Register your models here.
from .models import Cat, Toy, Feeding, Photo

admin.site.register([Cat, Toy, Feeding, Photo])
