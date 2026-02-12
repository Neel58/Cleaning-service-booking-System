from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('index/', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('profile/', views.user_profile, name='user_profile'),
    path('provider/dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('provider/update/<int:booking_id>/', views.provider_update, name='provider_update'),
    path('provider/profile/', views.provider_profile, name='provider_profile'),
    path('logout/', views.logout_view, name='logout'),
]
