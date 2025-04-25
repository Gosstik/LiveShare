"""
URL configuration for Backend project.

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

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



#############################################
### Friends


### APIView
# /users/v1/search          # search by email or username
# /users/v1/user/friends/friend/add
# /users/v1/user/friends
# /users/v1/user/friends/friend/delete
# TODO: accept invitation

#############################################
### Auth / Registration

# TODO: add existing
# /auth/v1/user/create
# /auth/v1/oauth/...
# /auth/v1/basic/...   # by password
# /auth/v1/logout

#############################################
### About

# ??? /about/v1/statistics

# schema_view = get_schema_view(
#     openapi.Info(
#         title="LiveShare API",
#         default_version="v1",
#         description="API for LiveShare web application",
#         terms_of_service="",
#         contact=openapi.Contact(email=""),
#         license=openapi.License(name="MIT License"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # App
    path("posts/", include("posts.urls")),
    path("comments/", include("comments.urls")),
    path("users/", include("users.urls")),
    path("auth/", include("custom_auth.urls")),
    ### Administrative
    path("admin/", admin.site.urls),
    # path(
    #     "swagger/",
    #     schema_view.with_ui("swagger", cache_timeout=0),
    #     name="schema-swagger-ui",
    # ),
    # Swagger
    path("api/schema/yaml", SpectacularAPIView.as_view(), name="yaml-api-schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="yaml-api-schema"),
        name="swagger-api-schema",
    ),
]

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
