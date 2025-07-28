"""
URL configuration for staticpatch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from staticpatchcore import views, views_admin, views_api

urlpatterns = [
    path("", views.index_view, name="index"),
    path("log_in", views.login_view, name="login"),
    path("log_out", views.logout_view, name="logout"),
    path(
        "site/<slug:site_slug>/build/<uuid:build_id>",
        views.site_build_detail_view,
        name="public_site_build_detail",
    ),
    # Admin
    path("admin", views_admin.admin_index_view, name="admin_index"),
    path("admin/site", views_admin.admin_site_list_view, name="admin_site_list"),
    path("admin/new_site", views_admin.admin_site_new_view, name="admin_site_new"),
    path(
        "admin/site/<slug:site_slug>",
        views_admin.admin_site_detail_view,
        name="admin_site_detail",
    ),
    path(
        "admin/site/<slug:site_slug>/edit",
        views_admin.admin_site_edit_view,
        name="admin_site_edit",
    ),
    path(
        "admin/site/<slug:site_slug>/build",
        views_admin.admin_site_build_list_view,
        name="admin_site_build_list",
    ),
    path(
        "admin/site/<slug:site_slug>/build/<uuid:build_id>",
        views_admin.admin_site_build_detail_view,
        name="admin_site_build_detail",
    ),
    path(
        "admin/site/<slug:site_slug>/build/<uuid:build_id>/delete",
        views_admin.admin_site_build_delete,
        name="admin_site_build_delete",
    ),
    path(
        "admin/site/<slug:site_slug>/new_security_key",
        views_admin.admin_site_new_security_key_view,
        name="admin_site_new_security_key",
    ),
    path(
        "admin/site/<slug:site_slug>/security_key/<uuid:security_key>/edit",
        views_admin.admin_site_security_key_edit,
        name="admin_site_security_key_edit",
    ),
    path(
        "admin/site/<slug:site_slug>/new_site_preview_type",
        views_admin.admin_site_new_preview_type_view,
        name="admin_site_new_preview_type",
    ),
    path(
        "admin/site/<slug:site_slug>/preview/<slug:preview_type_slug>",
        views_admin.admin_site_preview_type_detail_view,
        name="admin_site_preview_type_detail",
    ),
    path(
        "admin/site/<slug:site_slug>/preview/<slug:preview_type_slug>/edit",
        views_admin.admin_site_preview_type_edit_view,
        name="admin_site_preview_type_edit",
    ),
    path(
        "admin/site/<slug:site_slug>/new_basic_auth_user",
        views_admin.admin_site_new_basic_auth_user_view,
        name="admin_site_new_basic_auth_user",
    ),
    path(
        "admin/site/<slug:site_slug>/basic_auth_user/<username>/delete",
        views_admin.admin_site_basic_auth_user_delete,
        name="admin_site_basic_auth_user_delete",
    ),
    path(
        "admin/site/<slug:site_slug>/new_alternative_domain",
        views_admin.admin_site_new_alternative_domain_view,
        name="admin_site_new_alternative_domain",
    ),
    path(
        "admin/site/<slug:site_slug>/alternative_domain/<uuid:alternative_domain_id>",
        views_admin.admin_site_edit_alternative_domain_view,
        name="admin_site_edit_alternative_domain",
    ),
    path(
        "admin/site/<slug:site_slug>/sub_site/<uuid:sub_site_id>",
        views_admin.admin_site_sub_site_detail_view,
        name="admin_site_sub_site_detail",
    ),
    # API
    path(
        "api/site/<slug:site_slug>/publish_built_site",
        views_api.api_publish_built_site_view,
        name="publish_built_site",
    ),
    path(
        "api/site/<slug:site_slug>/deactivate",
        views_api.api_deactivate_view,
        name="api_deactivate",
    ),
    path(
        "api/site/<slug:site_slug>/preview/<slug:preview_type_slug>/instance/<slug:preview_instance_slug>"
        + "/publish_built_site",
        views_api.api_publish_built_site_preview_instance_view,
        name="publish_built_site",
    ),
    path(
        "api/site/<slug:site_slug>/preview/<slug:preview_type_slug>/instance/<slug:preview_instance_slug>/deactivate",
        views_api.api_site_preview_instance_deactivate_view,
        name="publish_built_site",
    ),
]
