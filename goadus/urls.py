# SPDX-PackageName: goadus-website
# SPDX-PackageSupplier: Ryan Finnie <ryan@finnie.org>
# SPDX-PackageDownloadLocation: https://github.com/finnix/goadus-website
# SPDX-FileCopyrightText: © 2020 Ryan Finnie <ryan@finnie.org>
# SPDX-License-Identifier: MPL-2.0

"""goadus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="goadus/login.html"),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(template_name="goadus/logout.html"),
        name="logout",
    ),
    path("admin/", admin.site.urls),
    path("api/upload/", views.api_upload, name="api-upload"),
    path("image/<slug>/", views.ImageView.as_view(), name="image"),
    path("imageset/<slug>/", views.ImageSetView.as_view(), name="imageset"),
    path("upload/", views.UploadView.as_view(), name="upload"),
    path("", views.index, name="index"),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.views.static import serve

    def serve_subdir_fn(request, path, document_root, **kwargs):
        path = "{}/{}/{}".format(path[0:1], path[1:2], path)
        return serve(request, path, document_root, **kwargs)

    urlpatterns += static(settings.MEDIA_URL, view=serve_subdir_fn, document_root=settings.MEDIA_ROOT)
