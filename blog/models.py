from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from .storage import VercelBlobStorage


def blog_image_path(instance, filename):
    """Generate path for blog images"""
    return f'blog_images/{instance.slug}/{filename}'


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('published', 'Published'),
        ('rejected', 'Rejected')
    )
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    edited_at = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    image = models.ImageField(
        upload_to=blog_image_path,
        storage=VercelBlobStorage() if settings.VERCEL else None,
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    moderator_note = models.TextField(
        blank=True, 
        null=True,
        help_text="Admin notes for rejected posts"
    )
    reviewed_by = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_posts'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
