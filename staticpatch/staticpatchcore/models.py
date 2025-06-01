import os
import uuid

from django.conf import settings
from django.db import models


class SiteModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    slug = models.CharField(max_length=500, null=False, unique=True)
    main_domain = models.CharField(max_length=500, null=False, unique=True)
    main_domain_ssl = models.BooleanField(null=False, default=True)
    basic_auth_user_required = models.BooleanField(null=False, default=False)
    allow_override = models.BooleanField(null=False, default=False)
    access_file_name = models.CharField(max_length=500, null=False, default=".htaccess")
    active = models.BooleanField(null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    deleted_at = models.DateTimeField(null=True)
    notes = models.TextField(null=True, blank=True)


class SiteAlternativeDomainModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    site = models.ForeignKey(SiteModel, on_delete=models.CASCADE, null=False)
    domain = models.CharField(max_length=500, null=False, unique=True)
    domain_ssl = models.BooleanField(null=False, default=True)
    active = models.BooleanField(null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    deleted_at = models.DateTimeField(null=True)
    notes = models.TextField(null=True, blank=True)


class SitePreviewTypeModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    site = models.ForeignKey(SiteModel, on_delete=models.CASCADE, null=False)
    slug = models.CharField(max_length=500, null=False, unique=False)
    domain = models.CharField(max_length=500, null=False)
    domain_ssl = models.BooleanField(null=False, default=True)
    basic_auth_user_required = models.BooleanField(null=False, default=False)
    active = models.BooleanField(null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    deleted_at = models.DateTimeField(null=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["site", "slug"],
                name="site_slug_unique",
            )
        ]


class SitePreviewInstanceModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    site_preview_type = models.ForeignKey(SitePreviewTypeModel, on_delete=models.CASCADE, null=False)
    slug = models.CharField(max_length=500, null=False, unique=False)
    active = models.BooleanField(null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["site_preview_type", "slug"],
                name="site_preview_type_slug_unique",
            )
        ]


class BuildModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    site = models.ForeignKey(SiteModel, on_delete=models.CASCADE, null=False)
    site_preview_instance = models.ForeignKey(SitePreviewInstanceModel, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)
    failed_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)

    def get_file_storage_slug(self) -> str:
        return self.created_at.strftime("%Y-%m-%d-%H-%M-%S") + "-" + str(self.id)

    def get_full_file_storage_directory(self) -> str:
        return os.path.join(
            settings.FILE_STORAGE,
            "site",
            str(self.site.id),
            "build",
            str(self.get_file_storage_slug()),
        )


class SiteSecurityKeyModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    site = models.ForeignKey(SiteModel, on_delete=models.CASCADE, null=False)
    key = models.CharField(max_length=500, null=False)
    active = models.BooleanField(null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    deleted_at = models.DateTimeField(null=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["site_id", "key"],
                name="site_id_key_unique",
            )
        ]


class BasicAuthUserModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    site = models.ForeignKey(SiteModel, on_delete=models.CASCADE, null=False)
    username = models.CharField(max_length=500, null=False)
    password_crypted = models.CharField(max_length=500, null=False)
    active = models.BooleanField(null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    deleted_at = models.DateTimeField(null=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["site_id", "username"],
                name="site_id_username_unique",
            )
        ]
