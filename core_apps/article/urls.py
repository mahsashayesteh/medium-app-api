from django.urls import path
from .views import ArticleListCreateView, ArticleRetrieveUpdateDestroyView, ClapView

urlpatterns = [
    path("", ArticleListCreateView.as_view(), name="article-list-create"),
    path("<uuid:id>/", ArticleRetrieveUpdateDestroyView.as_view(), 
         name="Article-retrive-update-destroy",),
    path("<uuid:article_id>/clap/", ClapView.as_view(), name="clapped_article" )
]