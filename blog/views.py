from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post, Category
from .forms import PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .storage import VercelBlobStorage
from django.conf import settings
import logging
from django.contrib import messages

logger = logging.getLogger(__name__)


def home(request):
    try:
        # Get posts based on user role
        if request.user.is_staff:
            posts_list = Post.objects.all().select_related('author', 'category')
        else:
            posts_list = Post.objects.filter(status='published').select_related('author', 'category')
        
        # Get total count before pagination
        total_posts = posts_list.count()
        
        # Add pagination
        paginator = Paginator(posts_list.order_by('-date_posted'), 6)  # 6 posts per page
        page = request.GET.get('page', 1)
        
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {
            'posts': posts,
            'posts_count': total_posts,  # Use total count from before pagination
            'page_obj': posts,  # For pagination template
        }
        
        return render(request, 'home.html', context)
        
    except Exception as e:
        logger.error(f"Error in home view: {e}")
        messages.error(request, "There was an error loading the page.")
        return render(request, 'home.html', {
            'posts': [],
            'posts_count': 0,
            'page_obj': None,
        })

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
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            # Handle image upload for Vercel
            if 'image' in request.FILES and settings.VERCEL:
                image = request.FILES['image']
                storage = VercelBlobStorage()
                path = f'blog_images/{post.slug}/{image.name}'
                url = storage._save(path, image)
                post.image = url
            
            if request.user.is_staff:
                post.status = 'published'
            else:
                post.status = 'pending'
                messages.info(request, 'Your post has been submitted for review.')
            
            post.save()
            
            if post.status == 'published':
                return redirect('post-detail', pk=post.pk)
            else:
                return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            
            # Handle image update for Vercel
            if 'image' in request.FILES and settings.VERCEL:
                # Delete old image if exists
                if post.image:
                    storage = VercelBlobStorage()
                    storage.delete(post.image)
                
                # Save new image
                image = request.FILES['image']
                storage = VercelBlobStorage()
                path = f'blog_images/{post.slug}/{image.name}'
                url = storage._save(path, image)
                post.image = url
            
            post.edited_at = timezone.now()
            post.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

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


def search(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query),
        status='published'
    ).order_by('-date_posted') if query else Post.objects.none()
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    categories = Category.objects.all()
    return render(request, 'blog/search_results.html', {
        'posts': posts,
        'query': query,
        'categories': categories,
    })

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published').order_by('-date_posted')
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    categories = Category.objects.all()
    return render(request, 'blog/category_posts.html', {
        'category': category,
        'posts': posts,
        'categories': categories,
    })

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you can add email sending logic
        # For now, we'll just show a success message
        messages.success(request, 'Thank you for your message! I\'ll get back to you soon.')
        return redirect('contact')
    
    return render(request, 'contact.html')
