from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from core_apps.article.models import Article

User = get_user_model()

class BookMarks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="bookmarks")
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name="bookmarks")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "article")
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.user.email} bookmark {self.article.title}"