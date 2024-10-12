from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from core_apps.common.models import TimeStampedModel
from .read_time_engin import ArticleReadTimeEngin

User = get_user_model()

class Article(TimeStampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, 
                               related_name="articles")
    title = models.CharField(max_length=255, verbose_name=_("عنوان"))
    slug = AutoSlugField(populate_from = "title", always_update=True, 
                         unique=True)
    description = models.CharField(max_length=255, verbose_name=_("توضیحات"))
    body = models.TextField(verbose_name=_("محتوای مقاله"))
    banner_image = models.ImageField(verbose_name=_("تصویر بنر"),
                                      default="/profile_defaul.png")
    tags = TaggableManager()

    def __str__(self):
        return f"{self.title} of {self.author.first_name}"
    
    @property
    def article_read_time(self):
        return ArticleReadTimeEngin.estimate_time_reading(self)
    
    @property
    def view_count(self):
        return self.article_view.count()
    
    def average_rating(self):
        ratings = self.rating.all()
        if ratings.count() > 0:
           total_rating = sum(rate.value for rate in ratings)
           average_rating = total_rating/ratings.count()
           return round(average_rating)
        return None
    
class ArticleView(TimeStampedModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, 
                                related_name="article_view")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name="user_views")
    viewer_ip = models.GenericIPAddressField(verbose_name=_("آی پی مشاهده کننده"),
                                             null=True, blank=True)
    
    class Meta:
        verbose_name = _("Article Views")
        verbose_name_plural = _("Article Views")
        unique_together = ("article", "user", "viewer_ip")

    def __str__(self):
        return f"{self.article.title} is viewed by {self.user.email if self.user else 'Anonymouse'} from IP {self.viewer_ip}"
    @classmethod
    def record_view(cls, article, user, viewer_ip):
        view,_ = cls.objects.get_or_create(article=article, user=user,
                                           viewer_ip=viewer_ip)
        view.save()

