from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
import logging
from django.contrib import messages
from django.core.paginator import Paginator

logger = logging.getLogger(__name__)


def home(request):
    if request.user.is_staff:
        # Staff can see all posts
        posts = Post.objects.all().order_by('-date_posted')
    else:
        # Regular users only see published posts
        posts = Post.objects.filter(status='published').order_by('-date_posted')
    
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    return render(request, 'home.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user can view this post
    if post.status != 'published' and not request.user.is_staff and request.user != post.author:
        messages.error(request, "This post is not available.")
        return redirect('home')
        
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Add request.FILES here
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            if request.user.is_staff:
                post.status = 'published'
            else:
                post.status = 'pending'
                messages.info(request, 'Your post has been submitted for review.')
            
            post.save()
            
            if post.status == 'published':
                return redirect('post-detail', pk=post.pk)
            else:
                return redirect('home')  # or create a "my posts" page
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})  # Change this line

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.edited_at = timezone.now()  # Only update edited_at
            post.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})  # Change this line too

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('home')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-date_posted')
    
    # Status filter
    status_filter = request.GET.get('status')
    if status_filter and status_filter != 'all':
        posts = posts.filter(status=status_filter)
    
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'posts': posts,
        'current_status': status_filter or 'all',
        'status_choices': Post.STATUS_CHOICES,
    }
    return render(request, 'blog/my_posts.html', context)