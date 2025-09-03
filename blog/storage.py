from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils.deconstruct import deconstructible
from vercel_blob import put, delete, list_blobs
import os
import mimetypes
from urllib.parse import urljoin

@deconstructible
class VercelBlobStorage(Storage):
    def __init__(self):
        self.client_token = settings.VERCEL_BLOB_CLIENT_TOKEN
        self.base_url = settings.MEDIA_URL

    def _save(self, name, content):
        """Save a file to Vercel Blob Storage"""
        content_type = mimetypes.guess_type(name)[0] or 'application/octet-stream'
        
        # Generate unique path
        path = self._generate_unique_path(name)
        
        # Upload to Vercel Blob
        blob = put(
            path,
            content,
            self.client_token,
            options={'access': 'public', 'contentType': content_type}
        )
        
        return blob.url

    def _open(self, name, mode='rb'):
        """Return a file object"""
        url = self.url(name)
        return ContentFile(url.encode())

    def delete(self, name):
        """Delete a file"""
        if name:
            try:
                delete(name, self.client_token)
            except Exception as e:
                print(f"Error deleting {name}: {e}")

    def exists(self, name):
        """Check if file exists"""
        try:
            blobs = list_blobs(self.client_token)
            return any(blob.pathname == name for blob in blobs)
        except:
            return False

    def url(self, name):
        """Return URL for accessing file"""
        if not name:
            return None
        
        # If already a full URL, return as is
        if name.startswith(('http://', 'https://')):
            return name
            
        return urljoin(self.base_url, name)

    def _generate_unique_path(self, name):
        """Generate unique path for file storage"""
        base, ext = os.path.splitext(name)
        return f"{base}_{os.urandom(8).hex()}{ext}"