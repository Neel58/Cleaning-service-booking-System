from django.contrib import admin
from .models import Service, UserProfile, Booking

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'price', 'duration', 'is_best_value')
    list_filter = ('service_type', 'is_best_value')
    search_fields = ('name', 'description')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone', 'city', 'rating', 'completed_jobs')
    list_filter = ('user_type',)
    search_fields = ('user__username', 'user__email', 'phone', 'city')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'provider', 'service', 'date_time', 'status', 'created_at')
    list_filter = ('status', 'service', 'created_at')
    search_fields = ('customer__username', 'provider__username', 'location')
    date_hierarchy = 'created_at'
