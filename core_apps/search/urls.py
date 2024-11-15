from django.urls import path
from .views import ArticleElasticSearchViewset

urlpatterns = [
    path("search/", ArticleElasticSearchViewset.as_view({"get":"list"}), name="article_search")
]