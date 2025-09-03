from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible
from django.conf import settings

@deconstructible
class VercelBlobStorage(FileSystemStorage):
    """
    Temporary fallback storage class while debugging Vercel Blob issues
    """
    def __init__(self):
        super().__init__(location=settings.MEDIA_ROOT)
        print("Warning: Using fallback storage instead of Vercel Blob")