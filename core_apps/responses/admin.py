from .models import Response
from django.contrib import admin

class ResponseAdmin(admin.ModelAdmin):
    list_display = ["pkid", "id", "user", "article", "parent_response", "content"
                    "created_at"]
    list_display_links = ["pkid", "id", "user"]