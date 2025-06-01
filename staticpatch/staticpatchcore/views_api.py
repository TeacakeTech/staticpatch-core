import os

from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

import staticpatchcore.models

from .tasks import process_build_task, update_server_config_task


@csrf_exempt
def api_publish_built_site_view(request, site_slug):
    # Check for common errors
    if "built_site" not in request.FILES:
        return HttpResponse("No File Attached", status=400)

    # Get Site
    try:
        site = staticpatchcore.models.SiteModel.objects.get(slug=site_slug)
    except staticpatchcore.models.SiteModel.DoesNotExist:
        return HttpResponse("Site not found", status=404)

    # Check Security code
    security_key = request.headers.get("Security-Key")
    if not security_key:
        return HttpResponse("No security key provided", status=403)

    try:
        staticpatchcore.models.SiteSecurityKeyModel.objects.get(
            site=site, key=security_key, active=True, deleted_at__isnull=True
        )
    except staticpatchcore.models.SiteSecurityKeyModel.DoesNotExist:
        return HttpResponse("Access Denied", status=403)

    # Save Build
    build = staticpatchcore.models.BuildModel(site=site)
    build.save()

    os.makedirs(build.get_full_file_storage_directory())

    file_name = os.path.join(build.get_full_file_storage_directory(), "site.zip")
    with open(file_name, "wb") as fp:
        for chunk in request.FILES["built_site"].chunks():
            fp.write(chunk)

    # Enqueue task
    process_build_task.enqueue(str(build.id))

    # Respond to user with build URL
    build_url = request.build_absolute_uri(reverse("public_site_build_detail", args=[site.slug, build.id]))
    return HttpResponse(build_url + "\n")


@csrf_exempt
def api_publish_built_site_preview_instance_view(request, site_slug, preview_type_slug, preview_instance_slug):
    # Check for common errors
    if "built_site" not in request.FILES:
        return HttpResponse("No File Attached", status=400)

    # Get Site
    try:
        site = staticpatchcore.models.SiteModel.objects.get(slug=site_slug)
    except staticpatchcore.models.SiteModel.DoesNotExist:
        return HttpResponse("Site not found", status=404)

    # Check Security code
    security_key = request.headers.get("Security-Key")
    if not security_key:
        return HttpResponse("No security key provided", status=403)

    try:
        staticpatchcore.models.SiteSecurityKeyModel.objects.get(
            site=site, key=security_key, active=True, deleted_at__isnull=True
        )
    except staticpatchcore.models.SiteSecurityKeyModel.DoesNotExist:
        return HttpResponse("Access Denied", status=403)

    # Get preview type
    try:
        preview_type_object = staticpatchcore.models.SitePreviewTypeModel.objects.get(
            site=site, slug=preview_type_slug, active=True, deleted_at__isnull=True
        )
    except staticpatchcore.models.SitePreviewTypeModel.DoesNotExist:
        return HttpResponse("Preview type not found", status=404)

    # Get Preview Instance
    try:
        site_preview_instance_object = staticpatchcore.models.SitePreviewInstanceModel.objects.get(
            site_preview_type=preview_type_object, slug=preview_instance_slug
        )
        # Ensure instance is active and not deleted
        site_preview_instance_object.active = True
        site_preview_instance_object.deleted_at = None
        site_preview_instance_object.save()
    except staticpatchcore.models.SitePreviewInstanceModel.DoesNotExist:
        # Create new instance if not found
        site_preview_instance_object = staticpatchcore.models.SitePreviewInstanceModel(
            site_preview_type=preview_type_object,
            slug=preview_instance_slug,
            active=True,
        )
        site_preview_instance_object.save()

    # Save Build
    build = staticpatchcore.models.BuildModel(site=site, site_preview_instance=site_preview_instance_object)
    build.save()

    os.makedirs(build.get_full_file_storage_directory())

    file_name = os.path.join(build.get_full_file_storage_directory(), "site.zip")
    with open(file_name, "wb") as fp:
        for chunk in request.FILES["built_site"].chunks():
            fp.write(chunk)

    # Enqueue task
    process_build_task.enqueue(str(build.id))

    # Respond to user with build URL
    build_url = request.build_absolute_uri(reverse("public_site_build_detail", args=[site.slug, build.id]))
    return HttpResponse(build_url + "\n")


@csrf_exempt
def api_site_preview_instance_deactivate_view(request, site_slug, preview_type_slug, preview_instance_slug):
    # Get Site
    try:
        site = staticpatchcore.models.SiteModel.objects.get(slug=site_slug)
    except staticpatchcore.models.SiteModel.DoesNotExist:
        return HttpResponse("Site not found", status=404)

    # Check Security code
    security_key = request.headers.get("Security-Key")
    if not security_key:
        return HttpResponse("No security key provided", status=403)

    try:
        staticpatchcore.models.SiteSecurityKeyModel.objects.get(
            site=site, key=security_key, active=True, deleted_at__isnull=True
        )
    except staticpatchcore.models.SiteSecurityKeyModel.DoesNotExist:
        return HttpResponse("Access Denied", status=403)

    # Get preview type
    try:
        preview_type_object = staticpatchcore.models.SitePreviewTypeModel.objects.get(
            site=site, slug=preview_type_slug, active=True, deleted_at__isnull=True
        )
    except staticpatchcore.models.SitePreviewTypeModel.DoesNotExist:
        return HttpResponse("Preview type not found", status=404)

    # Get Preview Instance
    try:
        site_preview_instance_object = staticpatchcore.models.SitePreviewInstanceModel.objects.get(
            site_preview_type=preview_type_object, slug=preview_instance_slug
        )
    except staticpatchcore.models.SitePreviewInstanceModel.DoesNotExist:
        return HttpResponse("Preview instance not found", status=404)

    # Finally do what we need to do
    site_preview_instance_object.active = False
    site_preview_instance_object.save()

    # Enqueue task
    update_server_config_task.enqueue()

    # Respond to user
    return HttpResponse("Thanks")
