from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    SERVICE_TYPES = [
        ('deep', 'Deep Cleaning'),
        ('sofa', 'Sofa Cleaning'),
        ('movein', 'Move-In Service'),
    ]
    
    name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50)
    is_best_value = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    USER_TYPES = [
        ('customer', 'Customer'),
        ('provider', 'Provider'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100, blank=True)
    experience_years = models.IntegerField(default=0, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    completed_jobs = models.IntegerField(default=0)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('work_started', 'Work Started'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_bookings')
    provider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='provider_bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    photo = models.ImageField(upload_to='booking_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.service.name} - {self.customer.username} - {self.status}"
