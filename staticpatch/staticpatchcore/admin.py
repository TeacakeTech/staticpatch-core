from django.contrib import admin

import staticpatchcore.models


@admin.register(staticpatchcore.models.SiteModel)
class SiteModelAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "main_domain", "active", "created_at")
    list_filter = ("active", "basic_auth_user_required", "allow_override")
    search_fields = ("slug", "main_domain", "notes")
    readonly_fields = ("id", "created_at")


@admin.register(staticpatchcore.models.SitePreviewTypeModel)
class SitePreviewTypeModelAdmin(admin.ModelAdmin):
    list_display = ("id", "site", "slug", "domain", "active")
    list_filter = ("active", "basic_auth_user_required", "domain_ssl")
    search_fields = ("slug", "domain", "notes")
    readonly_fields = ("id", "created_at")


@admin.register(staticpatchcore.models.SitePreviewInstanceModel)
class SitePreviewInstanceModelAdmin(admin.ModelAdmin):
    list_display = ("id", "site_preview_type", "slug", "active", "created_at")
    list_filter = ("active",)
    search_fields = ("slug",)
    readonly_fields = ("id", "created_at")


@admin.register(staticpatchcore.models.SiteSecurityKeyModel)
class SiteSecurityKeyModelAdmin(admin.ModelAdmin):
    list_display = ("id", "site", "active", "created_at")
    list_filter = ("active",)
    search_fields = ("notes",)
    readonly_fields = ("id", "created_at")


@admin.register(staticpatchcore.models.BasicAuthUserModel)
class BasicAuthUserModelAdmin(admin.ModelAdmin):
    list_display = ("id", "site", "username", "active", "created_at")
    list_filter = ("active",)
    search_fields = ("username", "notes")
    readonly_fields = ("id", "created_at")


@admin.register(staticpatchcore.models.SiteAlternativeDomainModel)
class SiteAlternativeDomainModelAdmin(admin.ModelAdmin):
    list_display = ("id", "site", "domain", "active", "created_at")
    list_filter = ("active", "domain_ssl")
    search_fields = ("domain", "notes")
    readonly_fields = ("id", "created_at")


@admin.register(staticpatchcore.models.BuildModel)
class BuildModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "site",
        "site_preview_instance",
        "created_at",
        "started_at",
        "finished_at",
        "failed_at",
    )
    list_filter = ("site",)
    search_fields = ("site__slug",)
    readonly_fields = ("id", "created_at", "started_at", "finished_at", "failed_at")
