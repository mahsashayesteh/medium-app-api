from django.conf import settings
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

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
]

admin.site.site_header = "Author Haven Api Admin"
admin.site.site_title = "Author Haven Api Admin Portal"
admin.site.index_title = "Welcome to Author Haven Api Portal"
