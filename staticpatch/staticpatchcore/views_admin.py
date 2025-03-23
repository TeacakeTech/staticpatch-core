from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

import staticpatchcore.models

from .forms import (
    EditSiteAlternativeDomainForm,
    EditSiteForm,
    EditSitePreviewTypeForm,
    NewBasicAuthUserForm,
    NewSiteAlternativeDomainForm,
    NewSiteForm,
    NewSitePreviewTypeForm,
    NewSiteSecurityKeyForm,
)
from .tasks import update_server_config_task
from .utils import crypt_apache_password


@login_required
def admin_index_view(request):
    return render(request, "staticpatchcore/admin/index.html")


@login_required
def admin_site_list_view(request):
    sites = staticpatchcore.models.SiteModel.objects.filter(deleted_at__isnull=True)
    return render(request, "staticpatchcore/admin/site.html", {"sites": sites})


@login_required
def admin_site_new_view(request):
    if request.method == "POST":
        form = NewSiteForm(request.POST)
        if form.is_valid():
            site = form.save()
            messages.success(request, "Site created successfully.")
            update_server_config_task.enqueue()
            return redirect("admin_site_detail", site_slug=site.slug)
    else:
        form = NewSiteForm()
    return render(request, "staticpatchcore/admin/new_site.html", {"form": form})


@login_required
def admin_site_detail_view(request, site_slug):
    site = get_object_or_404(staticpatchcore.models.SiteModel, slug=site_slug, deleted_at__isnull=True)
    preview_types = staticpatchcore.models.SitePreviewTypeModel.objects.filter(site=site, deleted_at__isnull=True)
    basic_auth_users = staticpatchcore.models.BasicAuthUserModel.objects.filter(site=site, deleted_at__isnull=True)
    security_keys = staticpatchcore.models.SiteSecurityKeyModel.objects.filter(site=site, deleted_at__isnull=True)
    alternative_domains = staticpatchcore.models.SiteAlternativeDomainModel.objects.filter(
        site=site, deleted_at__isnull=True
    )
    return render(
        request,
        "staticpatchcore/admin/site/index.html",
        {
            "site": site,
            "preview_types": preview_types,
            "basic_auth_users": basic_auth_users,
            "security_keys": security_keys,
            "alternative_domains": alternative_domains,
        },
    )


@login_required
def admin_site_edit_view(request, site_slug):
    site = get_object_or_404(staticpatchcore.models.SiteModel, slug=site_slug, deleted_at__isnull=True)
    if request.method == "POST":
        form = EditSiteForm(request.POST, instance=site)
        if form.is_valid():
            form.save()
            messages.success(request, "Site updated successfully.")
            update_server_config_task.enqueue()
            return redirect("admin_site_detail", site_slug=site.slug)
    else:
        form = EditSiteForm(instance=site)
    return render(
        request,
        "staticpatchcore/admin/site/edit.html",
        {"site": site, "form": form},
    )


@login_required
def admin_site_build_list_view(request, site_slug):
    site = get_object_or_404(staticpatchcore.models.SiteModel, slug=site_slug, deleted_at__isnull=True)
    builds = staticpatchcore.models.BuildModel.objects.filter(site=site).order_by("-created_at")
    return render(
        request,
        "staticpatchcore/admin/site/build.html",
        {"site": site, "builds": builds},
    )


@login_required
def admin_site_build_detail_view(request, site_slug, build_id):
    site = get_object_or_404(staticpatchcore.models.SiteModel, slug=site_slug, deleted_at__isnull=True)
    build = get_object_or_404(staticpatchcore.models.BuildModel, id=build_id, site=site)
    return render(
        request,
        "staticpatchcore/admin/site/build/index.html",
        {"site": site, "build": build},
    )


@login_required
def admin_site_new_security_key_view(request, site_slug):
    site = get_object_or_404(staticpatchcore.models.SiteModel, slug=site_slug, deleted_at__isnull=True)
    if request.method == "POST":
        form = NewSiteSecurityKeyForm(request.POST)
        if form.is_valid():
            security_key = form.save(commit=False)
            security_key.site = site
            security_key.save()
            messages.success(request, "Security key created successfully.")
            return render(
                request,
                "staticpatchcore/admin/site/new_security_key.done.html",
                {"site": site, "security_key": security_key},
            )
    else:
        form = NewSiteSecurityKeyForm()
    return render(
        request,
        "staticpatchcore/admin/site/new_security_key.html",
        {"site": site, "form": form},
    )


@login_required
def admin_site_security_key_edit(request, site_slug, security_key):
    site = get_object_or_404(staticpatchcore.models.SiteModel, slug=site_slug)
    security_key_obj = get_object_or_404(
        staticpatchcore.models.SiteSecurityKeyModel,
        id=security_key,
        site=site,
        deleted_at__isnull=True,
    )

    if request.method == "POST":
        security_key_obj.active = request.POST.get("active") == "on"
        security_key_obj.notes = request.POST.get("notes", "")
        security_key_obj.save()
        messages.success(request, "Security key updated successfully")
        return redirect("admin_site_detail", site_slug=site.slug)

    return render(
        request,
        "staticpatchcore/admin/site/securitykey/edit.html",
        {
            "site": site,
            "security_key": security_key_obj,
        },
    )


@login_required
def admin_site_new_preview_type_view(request, site_slug):
    site = get_object_or_404(staticpatchcore.models.SiteModel, slug=site_slug, deleted_at__isnull=True)
    if request.method == "POST":
        form = NewSitePreviewTypeForm(request.POST)
        if form.is_valid():
            preview_type = form.save(commit=False)
            preview_type.site = site
            preview_type.save()
            messages.success(request, "Preview type created successfully.")
            return redirect("admin_site_detail", site_slug=site.slug)
    else:
        form = NewSitePreviewTypeForm()
    return render(
        request,
        "staticpatchcore/admin/site/new_preview_type.html",
        {"site": site, "form": form},
    )


@login_required
def admin_site_preview_type_detail_view(request, site_slug, preview_type_slug):
    site = get_object_or_404(staticpatchcore.models.SiteModel, slug=site_slug, deleted_at__isnull=True)
    preview_type = get_object_or_404(
        staticpatchcore.models.SitePreviewTypeModel,
        site=site,
        slug=preview_type_slug,
        deleted_at__isnull=True,
    )
    preview_instances = staticpatchcore.models.SitePreviewInstanceModel.objects.filter(
        site_preview_type=preview_type
    ).order_by("-created_at")
    return render(
        request,
        "staticpatchcore/admin/site/preview/index.html",
        {
            "site": site,
            "preview_type": preview_type,
            "preview_instances": preview_instances,
        },
    )


@login_required
def admin_site_preview_type_edit_view(request, site_slug, preview_type_slug):
    site = get_object_or_404(staticpatchcore.models.SiteModel, slug=site_slug, deleted_at__isnull=True)
    preview_type = get_object_or_404(
        staticpatchcore.models.SitePreviewTypeModel,
        site=site,
        slug=preview_type_slug,
        deleted_at__isnull=True,
    )

    if request.method == "POST":
        form = EditSitePreviewTypeForm(request.POST, instance=preview_type)
        if form.is_valid():
            form.save()
            messages.success(request, "Preview type updated successfully")
            update_server_config_task.enqueue()
            return redirect(
                "admin_site_preview_type_detail",
                site_slug=site_slug,
                preview_type_slug=preview_type_slug,
            )
    else:
        form = EditSitePreviewTypeForm(instance=preview_type)

    return render(
        request,
        "staticpatchcore/admin/site/preview/edit.html",
        {"site": site, "preview_type": preview_type, "form": form},
    )


@login_required
def admin_site_new_basic_auth_user_view(request, site_slug):
    site = get_object_or_404(staticpatchcore.models.SiteModel, slug=site_slug, deleted_at__isnull=True)
    if request.method == "POST":
        form = NewBasicAuthUserForm(request.POST)
        if form.is_valid():
            basic_auth_user = form.save(commit=False)
            basic_auth_user.site = site
            basic_auth_user.password_crypted = crypt_apache_password(form.cleaned_data["password_crypted"])
            basic_auth_user.save()
            messages.success(request, "Basic auth user created successfully.")
            update_server_config_task.enqueue()
            return redirect("admin_site_detail", site_slug=site.slug)
    else:
        form = NewBasicAuthUserForm()
    return render(
        request,
        "staticpatchcore/admin/site/new_basic_auth_user.html",
        {"site": site, "form": form},
    )


@login_required
def admin_site_new_alternative_domain_view(request, site_slug):
    site = get_object_or_404(staticpatchcore.models.SiteModel, slug=site_slug, deleted_at__isnull=True)
    if request.method == "POST":
        form = NewSiteAlternativeDomainForm(request.POST)
        if form.is_valid():
            alternative_domain = form.save(commit=False)
            alternative_domain.site = site
            alternative_domain.save()
            messages.success(request, "Alternative domain created successfully.")
            update_server_config_task.enqueue()
            return redirect("admin_site_detail", site_slug=site.slug)
    else:
        form = NewSiteAlternativeDomainForm()
    return render(
        request,
        "staticpatchcore/admin/site/new_alternative_domain.html",
        {"site": site, "form": form},
    )


@login_required
def admin_site_edit_alternative_domain_view(request, site_slug, alternative_domain_id):
    site = get_object_or_404(staticpatchcore.models.SiteModel, slug=site_slug, deleted_at__isnull=True)
    alternative_domain = get_object_or_404(
        staticpatchcore.models.SiteAlternativeDomainModel,
        id=alternative_domain_id,
        site=site,
        deleted_at__isnull=True,
    )
    if request.method == "POST":
        form = EditSiteAlternativeDomainForm(request.POST, instance=alternative_domain)
        if form.is_valid():
            form.save()
            messages.success(request, "Alternative domain updated successfully.")
            update_server_config_task.enqueue()
            return redirect("admin_site_detail", site_slug=site.slug)
    else:
        form = EditSiteAlternativeDomainForm(instance=alternative_domain)
    return render(
        request,
        "staticpatchcore/admin/site/alternative_domain/edit.html",
        {"site": site, "alternative_domain": alternative_domain, "form": form},
    )
