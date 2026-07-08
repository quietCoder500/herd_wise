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

urlpatterns = [
    path("", include("apps.pages.urls")),
    path("admin/", admin.site.urls),
    path("accounts/signup/", StandardSignupView.as_view(), name="account_signup"),
    path("accounts/", include("allauth.urls")),
    path(
        "portal/",
        include(("apps.portal.urls", "portal"), namespace="portal"),
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
/portal/farms/<str:public_id>                     # farms/farms_view.html

/portal/farms/<str:public_id>/forms               # forms/forms_list.html
/portal/farms/<str:public_id>/forms/create        # forms/forms_create.html

/portal/farms/<str:public_id>/herds/              # herds/herds_list.html
/portal/farms/<str:public_id>/herds/create        # herds/herds_create.html
/portal/herds/<str:public_id>                     # herds/herds_view.html

/portal/herds/<str:public_id>/records             # records/records_list.html
/portal/herds/<str:public_id>/records/create      # records/records_create.html 

/portal/herds/<str:public_id>/animals/            # animals/animals_list.html
/portal/herds/<str:public_id>/animals/create      # animals/animals_create.html
/portal/animals/<str:public_id>                   # animals/animals_view.html

/portal/animals/<str:public_id>/records           # records/records_list.html
/portal/animals/<str:public_id>/records/create    # records/records_create.html

/portal/records                                   # records/records_list.html
/portal/records/<str:public_id>                   # records/records_view.html
"""
