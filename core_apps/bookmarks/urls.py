from django.urls import path
from .views import BookMarksDestroyedView, BookMarksCreateView

urlpatterns = [
    path("bookmark_article/<uuid:article_id>", BookMarksCreateView.as_view(), name="bookmark_article"),
    path("remove_bookmark/<uuid:article_id>", BookMarksDestroyedView.as_view(), name="remove_bookmark")
]