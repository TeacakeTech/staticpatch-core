import os
import shutil

from django.conf import settings
from django.utils import timezone

from .models import BasicAuthUserModel, BuildModel


def purge_deleted():
    """
    Purge deleted objects that are older than PURGE_DELETED_AFTER_SECONDS.
    """
    cutoff_time = timezone.now() - timezone.timedelta(seconds=settings.PURGE_DELETED_AFTER_SECONDS)
    # Basic Auth Users
    BasicAuthUserModel.objects.filter(deleted_at__isnull=False, deleted_at__lt=cutoff_time).delete()
    # Builds
    for build in BuildModel.objects.filter(deleted_at__isnull=False, deleted_at__lt=cutoff_time):
        dir_name = build.get_full_file_storage_directory()
        build.delete()
        if os.path.isdir(dir_name):
            shutil.rmtree(dir_name)
