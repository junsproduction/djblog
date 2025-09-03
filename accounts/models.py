from django.db import models
from django.contrib.auth.models import AbstractUser
from blog.storage import VercelBlobStorage
from django.conf import settings
from django.utils import timezone
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

def profile_pic_path(instance, filename):
    """Generate path for profile pictures"""
    return f'profile_pics/{instance.username}/{filename}'

def get_storage():
    """Helper function to determine storage backend"""
    return VercelBlobStorage() if getattr(settings, 'VERCEL', False) else None

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('author', 'Author'),
        ('subscriber', 'Subscriber'),
    )
    
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        storage=get_storage(),
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.full_name or self.email

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='subscriber')
