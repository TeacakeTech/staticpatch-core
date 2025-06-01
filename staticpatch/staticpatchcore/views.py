from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render

import staticpatchcore.models


def index_view(request):
    return render(request, "staticpatchcore/index.html")


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "staticpatchcore/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("index")


def site_build_detail_view(request, site_slug, build_id):
    site = get_object_or_404(staticpatchcore.models.SiteModel, slug=site_slug, deleted_at__isnull=True)
    build = get_object_or_404(staticpatchcore.models.BuildModel, id=build_id, site=site, deleted_at__isnull=True)
    return render(request, "staticpatchcore/site/build/index.html", {"site": site, "build": build})
