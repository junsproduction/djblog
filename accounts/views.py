from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileEditForm
from .utils import send_password_notification
from blog.models import Post
from django.contrib.auth import update_session_auth_hash

User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.get_user()
            login(request, email)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def user_profile(request, username):
    # Get the user model and profile
    User = get_user_model()
    user_profile = get_object_or_404(User, full_name=username)
    posts = Post.objects.filter(author=user_profile).order_by('-date_posted')
    
    # Handle form submission (POST request)
    if request.method == 'POST' and request.user == user_profile:
        form = ProfileEditForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            # Save directly since imagekit handles the processing
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile', username=user_profile.full_name)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileEditForm(instance=user_profile)
    
    context = {
        'user_profile': user_profile,
        'posts': posts,
        'form': form,
        'is_owner': request.user == user_profile
    }
    
    return render(request, 'accounts/user_profile.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            
            try:
                send_password_notification(user, 'changed')
                messages.success(request, 'Your password was successfully updated!')
            except Exception as e:
                messages.warning(request, 'Password updated but email notification failed.')
                
            return redirect('change_password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})
