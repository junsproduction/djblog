from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils.deconstruct import deconstructible
from vercel_blob import Client

@deconstructible
class VercelBlobStorage(Storage):
    def __init__(self):
        self.client_token = settings.VERCEL_BLOB_CLIENT_TOKEN
        self.blob_client = Client({'token': self.client_token})

    def _save(self, name, content):
        """Save a file to Vercel Blob Storage"""
        blob = self.blob_client.upload(content, name)
        return blob.url

    def _open(self, name, mode='rb'):
        """Return a file object"""
        url = self.url(name)
        return ContentFile(url.encode())

    def delete(self, name):
        """Delete a file"""
        if name:
            self.blob_client.delete(name)

    def exists(self, name):
        """Check if file exists"""
        try:
            blobs = self.blob_client.list()
            return any(blob.pathname == name for blob in blobs)
        except:
            return False

    def url(self, name):
        """Return URL for accessing file"""
        if not name:
            return None
        if name.startswith(('http://', 'https://')):
            return name
        return f"{settings.MEDIA_URL.rstrip('/')}/{name.lstrip('/')}"