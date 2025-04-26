from django.conf import settings
from django.utils import timezone

from .models import BasicAuthUserModel


def purge_deleted():
    """
    Purge deleted objects that are older than PURGE_DELETED_AFTER_SECONDS.
    """
    cutoff_time = timezone.now() - timezone.timedelta(seconds=settings.PURGE_DELETED_AFTER_SECONDS)
    # Basic Auth Users
    BasicAuthUserModel.objects.filter(deleted_at__isnull=False, deleted_at__lt=cutoff_time).delete()
