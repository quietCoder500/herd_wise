"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.users.views import StandardSignupView
from apps.portal.views import tags_link_redirect
from apps.export.views import export_herd_weights_zip, export_herd_weights_pdf

urlpatterns = [
    path("", include("apps.pages.urls")),
    path("admin/", admin.site.urls),
    path("accounts/signup/", StandardSignupView.as_view(), name="account_signup"),
    path("tag/<slug:slug>/", tags_link_redirect, name="tag_redirect"),
    path("accounts/", include("allauth.urls")),
    path(
        "portal/",
        include(("apps.portal.urls", "portal"), namespace="portal"),
    ),
    path(
        "export-weights/<slug:template_slug>/<slug:herd_slug>/",
        export_herd_weights_zip,
        name="export_herd_weights_zip",
    ),
    path(
        "export-pdf/<slug:template_slug>/<slug:herd_slug>/",
        export_herd_weights_pdf,
        name="export_herd_weights_pdf",
    ),
]

if settings.DEBUG:
    # Include django_browser_reload URLs only in DEBUG mode
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


"""
/portal/                                          # index.html
/portal/search/                                   # search.html
/portal/farms/                                    # farms/farms_list.html
/portal/farms/create                              # farms/farms_create.html
/portal/farms/<str:slug>                     # farms/farms_view.html

/portal/farms/<str:slug>/forms               # forms/forms_list.html
/portal/farms/<str:slug>/forms/create        # forms/forms_create.html
/portal/farms/<str:slug>/forms/<slug:form_slug>        # forms/forms_view.html

/portal/farms/<str:slug>/herds/              # herds/herds_list.html
/portal/farms/<str:slug>/herds/create        # herds/herds_create.html
/portal/herds/<str:slug>                     # herds/herds_view.html

/portal/herds/<str:slug>/records             # records/records_list.html
/portal/herds/<str:slug>/records/<slug:form_slug>      # records/records_create.html 

/portal/herds/<str:slug>/animals/            # animals/animals_list.html
/portal/herds/<str:slug>/animals/create      # animals/animals_create.html
/portal/animals/<str:slug>                   # animals/animals_view.html

/portal/animals/<str:slug>/records           # records/records_list.html
/portal/animals/<str:slug>/records/<slug:form_slug>    # records/records_create.html

/portal/records                                   # records/records_list.html
/portal/records/<str:slug>                   # records/records_view.html
"""
