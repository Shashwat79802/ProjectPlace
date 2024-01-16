from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """Defines the settings to store static files of the application."""

    location = 'app_static_files'
    default_acl = 'public-read'

class PublicMediaStorage(S3Boto3Storage):
    """Defines the settings to store media files of the application."""

    default_acl = 'public-read'
    file_overwrite = 'true'


class PublicImageStorage(PublicMediaStorage):
    """Defines the settings to store media files of the application."""

    location = 'project-images'


class PublicDocumentStorage(PublicMediaStorage):
    """Defines the settings to store media files of the application."""

    location = 'project-documents'
