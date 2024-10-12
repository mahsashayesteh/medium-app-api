from core_apps.article.models import Article
from django.utils.translation import gettext_lazy as _
from core_apps.users.models import User
from core_apps.common.models import TimeStampedModel
from django.db import models


class Rating(TimeStampedModel):
    class Range(models.IntegerChoices):
        RATING_1 = 1, _("poor")
        RATING_2 = 2, _("fair")
        RATING_3 = 3, _("good")
        RATING_4 = 4, _("very good")
        RATING_5 = 5, _("excellent")

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user")
    article = models.ForeignKey(Article, related_name="rating",
                                 on_delete=models.CASCADE)
    value = models.IntegerField(
        verbose_name=_("rating value"),
        choices=Range.choices,
        default=0,
        help_text="1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent",
    )
    review = models.TextField(blank=True)

    class Meta:
        unique_together = ("user", "value")
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"

    def __str__(self):
        return f"{self.user.name} rated {self.article.title} as {self.get_rating_display()}"
    
    