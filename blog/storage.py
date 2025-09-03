from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils.deconstruct import deconstructible
from vercel_blob import put, delete, list_blobs, PutOptions

@deconstructible
class VercelBlobStorage(Storage):
    def __init__(self):
        self.client_token = settings.VERCEL_BLOB_CLIENT_TOKEN

    def _save(self, name, content):
        options = PutOptions(access='public')
        blob = put(name, content, self.client_token, options)
        return blob.url

    def _open(self, name, mode='rb'):
        """Return a file object"""
        url = self.url(name)
        return ContentFile(url.encode())

    def delete(self, name):
        """Delete a file"""
        if name:
            delete(name, self.client_token)

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
        if name.startswith(('http://', 'https://')):
            return name
        return f"{settings.MEDIA_URL.rstrip('/')}/{name.lstrip('/')}"