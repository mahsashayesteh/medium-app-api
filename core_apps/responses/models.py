from core_apps.common.models import TimeStampedModel
from django.db import models
from core_apps.article.models import Article
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Response(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                             related_name="responses")
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name="responses")
    parent_response = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replies",
        null=True,
        blank=True
        )
    
    content = models.TextField(verbose_name=_("متن"))

    class Meta:
        verbose_name = _("کامنت")
        verbose_name_plural = _("کامنت ها")
        ordering = ["created_at"]
    
    def __str__(self):
        return f'{self.user.email} commmented on {self.article.title}'
