from django.contrib import admin
from .models import Article, ArticleView

class ArticleAdmin(admin.ModelAdmin):
    list_display = ["pkid", "author", "title", "slug"]
    list_display_links = ["pkid", "author"]
    list_filter = ["created_at"]
    search_fields = ["title", "body", "tags"]
    ordering = ["-created_at"]

class ArticleViewAdmin(admin.ModelAdmin):
    list_display = ["pkid", "article", "user"]
    list_display_links = ["pkid", "article"]
    list_filter = ["created_at"]
    search_fields = ["article", "user"]

admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleView, ArticleViewAdmin)
    
