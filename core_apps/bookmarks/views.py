from .models import BookMarks
from core_apps.article.models import Article
from .serializers import BookMarkSerializer
from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound, ValidationError
from django.db import IntegrityError
from uuid import UUID

class BookMarksCreateView(generics.CreateAPIView):
    queryset = BookMarks.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookMarkSerializer

    def perform_create(self, serializer):
        article_id = self.kwargs.get("article_id")
        
        if article_id:
            try:
               article = Article.objects.get(id=article_id)
            except Article.DoesNotExist:
                raise ValidationError("Invalid article id provided")
        else:
            raise ValidationError("article_id is required")
        
        try:
            serializer.save(user = self.request.user,
                                            article = article )
        except IntegrityError:
            raise ValidationError("you have already bookmarked this article")
        

class BookMarksDestroyedView(generics.DestroyAPIView):
    queryset = BookMarks.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookMarkSerializer
    lookup_field = "article_id"
    
    def get_object(self):
        user = self.request.user
        article_id = self.kwargs.get("article_id")
        
        try: 
            UUID(str(article_id), version=4)
            
        except ValueError:
            raise ValidationError("Invalid article_id provided")
        
        try:
            
            bookmark = BookMarks.objects.get(user=user, article__id=article_id)
        except BookMarks.DoesNotExist:
            raise NotFound("Bookmark not found or it doesn't belong to you")
        
        return bookmark
    
    def perform_destroy(self, instance):
        user = self.request.user
         
        if user != instance.user:
            raise ValidationError("You cannot delete bookmarks of other users ")
        instance.delete()
        