from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.utils import timezone
from blog.models import Post, Category
from .decorators import staff_required, superuser_required
from blog.utils import send_moderation_email
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import timedelta

@staff_required
def dashboard(request):
    """Main dashboard view for staff members"""
    User = get_user_model()
    
    # Get date range (last 30 days)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    
    # User registration data
    user_stats = (
        User.objects.filter(date_joined__range=(start_date, end_date))
        .annotate(date=TruncDate('date_joined'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    
    # Post creation data
    post_stats = (
        Post.objects.filter(date_posted__range=(start_date, end_date))
        .annotate(date=TruncDate('date_posted'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    
    context = {
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(is_active=True).count(),
        'total_posts': Post.objects.count(),
        'total_categories': Category.objects.count(),
        'user_labels': [str(stat['date']) for stat in user_stats],
        'user_data': [stat['count'] for stat in user_stats],
        'post_labels': [str(stat['date']) for stat in post_stats],
        'post_data': [stat['count'] for stat in post_stats],
    }
    return render(request, 'dashboard/dashboard.html', context)

@staff_required
def user_list(request):
    User = get_user_model()
    users = User.objects.all().order_by('-date_joined')
    paginator = Paginator(users, 10)
    page = request.GET.get('page')
    users = paginator.get_page(page)
    return render(request, 'dashboard/users.html', {'users': users})

@staff_required
def post_management(request):
    """Post management view"""
    posts = Post.objects.all().order_by('-date_posted')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'dashboard/posts.html', {'posts': posts})

@superuser_required
def user_edit(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        role = request.POST.get('role')
        is_active = request.POST.get('is_active') == 'true'
        is_staff = request.POST.get('is_staff') == 'true'
        
        # Prevent superuser from being demoted
        if user.is_superuser and user != request.user:
            messages.error(request, "Superuser status cannot be modified")
            return redirect('dashboard:users')
            
        user.role = role
        user.is_active = is_active
        user.is_staff = is_staff
        user.save()
        
        messages.success(request, f"User {user.full_name} has been updated")
        return redirect('dashboard:users')
        
    return render(request, 'dashboard/user_edit.html', {'edit_user': user})

@superuser_required
def user_delete(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    
    if user.is_superuser:
        messages.error(request, "Superuser cannot be deleted")
        return redirect('dashboard:users')
        
    user.delete()
    messages.success(request, f"User {user.full_name} has been deleted")
    return redirect('dashboard:users')

@staff_required
def moderate_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if request.method == 'POST':
        old_status = post.status
        status = request.POST.get('status')
        note = request.POST.get('moderator_note')
        
        post.status = status
        post.moderator_note = note
        post.reviewed_by = request.user
        post.reviewed_at = timezone.now()
        post.save()
        
        # Send email notification
        try:
            send_moderation_email(post, status, note)
            messages.success(
                request, 
                f'Post "{post.title}" has been moderated and author notified.'
            )
        except Exception as e:
            messages.error(
                request, 
                f'Post moderated but email notification failed: {str(e)}'
            )
            
    return redirect('dashboard:posts')