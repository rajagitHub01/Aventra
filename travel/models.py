from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    address = models.TextField()
    def __str__(self):
        return self.user.username


class Package(models.Model):
    PACKAGE_TYPE=[
        ('domestic', 'Domestic'),
        ('international', 'International')
    ]
    title = models.CharField(max_length = 100)
    location = models.CharField(max_length = 50)
    price = models.IntegerField()
    original_price = models.IntegerField(null = True, blank = True)
    discount_percent = models.IntegerField(null = True, blank = True)
    duration = models.CharField(max_length = 100)
    stay_plan = models.CharField(max_length = 120, blank = True)
    description = models.CharField(max_length = 150)
    image = models.ImageField(upload_to = 'packages/')
    package_type = models.CharField(max_length = 20, choices = PACKAGE_TYPE)
    created_at = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.title

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    package = models.ForeignKey(Package, on_delete = models.CASCADE)
    booking_date = models.DateField()
    persons = models.IntegerField()
    total_price = models.IntegerField()
    status = models.CharField(max_length = 20, default = 'pending')

class Review(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    package = models.ForeignKey(Package, on_delete = models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)



