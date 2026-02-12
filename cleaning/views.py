from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Service, UserProfile, Booking

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        user_type = request.POST.get('user_type')
        phone = request.POST.get('phone')
        
        # Validation
        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
            return render(request, 'cleaning/signup.html')
        
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'cleaning/signup.html')
        
        if not user_type:
            messages.error(request, 'Please select a user type')
            return render(request, 'cleaning/signup.html')
        
        try:
            # Create user with email as username
            user = User.objects.create_user(username=email, email=email, password=password)
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                user_type=user_type,
                phone=phone
            )
            
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'cleaning/signup.html')
    
    return render(request, 'cleaning/signup.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            try:
                profile = UserProfile.objects.get(user=user)
                
                if user_type == 'customer' and profile.user_type == 'customer':
                    login(request, user)
                    return redirect('index')
                elif user_type == 'provider' and profile.user_type == 'provider':
                    login(request, user)
                    return redirect('provider_dashboard')
                else:
                    messages.error(request, 'Invalid user type for this account')
            except UserProfile.DoesNotExist:
                messages.error(request, 'User profile not found')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'cleaning/login.html')

@login_required
def index(request):
    return render(request, 'cleaning/index.html')

@login_required
def services(request):
    services_list = Service.objects.all()
    return render(request, 'cleaning/services.html', {'services': services_list})

@login_required
def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'POST':
        date_time = request.POST.get('date_time')
        
        booking = Booking.objects.create(
            customer=request.user,
            service=service,
            date_time=date_time,
            location='Hostel Block A',
            status='confirmed'
        )
        messages.success(request, 'Booking confirmed!')
        return redirect('user_profile')
    
    return render(request, 'cleaning/service_detail.html', {'service': service})

@login_required
def user_profile(request):
    bookings = Booking.objects.filter(customer=request.user)
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    return render(request, 'cleaning/user_profile.html', {
        'bookings': bookings,
        'profile': profile
    })

@login_required
def provider_dashboard(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found')
        return redirect('login')
    
    if profile.user_type != 'provider':
        return redirect('index')
    
    new_requests = Booking.objects.filter(status='pending')
    active_jobs = Booking.objects.filter(provider=request.user, status__in=['confirmed', 'in_progress', 'work_started'])
    
    if request.method == 'POST':
        action = request.POST.get('action')
        booking_id = request.POST.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id)
        
        if action == 'accept':
            booking.provider = request.user
            booking.status = 'confirmed'
            booking.save()
            messages.success(request, 'Job accepted!')
        elif action == 'reject':
            booking.status = 'cancelled'
            booking.save()
            messages.success(request, 'Job rejected')
    
    return render(request, 'cleaning/provider_dashboard.html', {
        'new_requests': new_requests,
        'active_jobs': active_jobs
    })

@login_required
def provider_update(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, provider=request.user)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        notes = request.POST.get('notes')
        photo = request.FILES.get('photo')
        
        booking.status = status
        booking.notes = notes
        if photo:
            booking.photo = photo
        booking.save()
        
        messages.success(request, 'Status updated successfully!')
        return redirect('provider_dashboard')
    
    return render(request, 'cleaning/provider_update.html', {'booking': booking})

@login_required
def provider_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found')
        return redirect('login')
    
    if profile.user_type != 'provider':
        return redirect('index')
    
    return render(request, 'cleaning/provider_profile.html', {'profile': profile})

def logout_view(request):
    logout(request)
    return redirect('login')
