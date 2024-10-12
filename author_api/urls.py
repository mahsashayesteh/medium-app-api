from django.conf import settings
from django.contrib import admin
from django.urls import (
    path,
    include,
    )
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from dj_rest_auth.views import PasswordResetConfirmView
from core_apps.users.views import CustomUserDetailView
from allauth.account.views import confirm_email as allauthemailconfirmation

schema_view = get_schema_view(
    openapi.Info(
       title="Author Haven Api",
       default_version="V1",
       description= "Api Endpoint for Author Haven",
       contact=openapi.Contact(email="mahsa.zohdi96@gmail.com",),
       license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),

)

urlpatterns = [
    path("redoc", schema_view.with_ui("redoc", cache_timeout=0)),
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/auth/user", CustomUserDetailView.as_view(), name="user_detail"),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    
    path("api/v1/auth/accounts/", include('allauth.urls')),
    path(
        "api/v1/auth/password/reset/cofirm/<uidb64>/<token>/",
         PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"
         ),
    path("api/v1/profiles/", include("core_apps.profiles.urls") ),
    path("api/v1/articles/", include("core_apps.article.urls")),
    path("api/v1/rating/", include("core_apps.rating.urls")),

]

admin.site.site_header = "Author Haven Api Admin"
admin.site.site_title = "Author Haven Api Admin Portal"
admin.site.index_title = "Welcome to Author Haven Api Portal"
