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
    REGION_CHOICE = [
        ('north', 'North India'),
        ('west', 'West India'),
        ('south', 'South India'),
        ('northeast', 'North-East India'),
    ]
    REGION_CHOICES = [
        ('europe', 'Europe'),
        ('southeast_asia', 'Southeast Asia'),
        ('middle_east', 'Middle East'),
        ('maldives', 'Maldives'),
        ('usa', 'USA'),
        ('dubai', 'Dubai'),
    ]
    title = models.CharField(max_length = 100)
    location = models.CharField(max_length = 50)
    price = models.IntegerField()
    original_price = models.IntegerField(null = True, blank = True)
    discount_percent = models.IntegerField(null = True, blank = True)
    duration = models.CharField(max_length = 100)
    stay_plan = models.CharField(max_length = 120, blank = True)
    description = models.TextField()
    image = models.ImageField(upload_to = 'packages/')
    package_type = models.CharField(max_length = 20, choices = PACKAGE_TYPE)
    region = models.CharField(max_length = 20, choices = REGION_CHOICE, blank=True, null=True)
    region_international = models.CharField(max_length=50, choices=REGION_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    is_trending = models.BooleanField(default = False)
    highlights = models.TextField(blank=True)
    confirmation_policy = models.TextField(default="Booking confirmation is subject to availability at the time of reservation. A confirmation voucher will be shared within 24 hours of successful payment.In case of non-availability, an alternative option of similar category will be provided.")
    refund_policy = models.TextField(default="Refunds (if applicable) will be processed within 7–10 working days. Transaction charges or gateway fees may be deducted. No refund will be provided for partially utilized services.")
    cancellation_policy = models.TextField(default="Free cancellation up to 7 days before travel date. 50% cancellation charges between 3–7 days before travel. No refund for cancellations within 48 hours of departure. No-show bookings are non-refundable.")
    payment_policy = models.TextField(default="A minimum of 30% advance payment is required to confirm the booking. Full payment must be completed before the start of the trip. Payments can be made via UPI, bank transfer, or online payment gateway.")
    

    itinerary = models.TextField(blank=True)
    def __str__(self):
        return self.title
    
class PackageImage(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='package_gallery/')

    def __str__(self):
        return self.package.title
    
class Highlight(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='highlights_list')
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    
class ItineraryDay(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='itinerary_days')
    day_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return f"Day {self.day_number} - {self.title}"
    
class Inclusion(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="inclusions_list")
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Exclusion(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="exclusions_list")
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    package = models.ForeignKey(Package, on_delete = models.CASCADE)
    booking_date = models.DateField()
    persons = models.IntegerField()
    total_price = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    package = models.ForeignKey(Package, on_delete = models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)



