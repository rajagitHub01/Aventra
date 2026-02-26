from django.contrib import admin
from .models import Package, Booking, Review, Profile

# Register your models here.
admin.site.register(Package)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Profile)
