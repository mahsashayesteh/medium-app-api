from rest_framework import generics, permissions
from .models import Rating
from .exception import AlreadyHaveRating
from .serializers import RatingSerializer
from django.db import IntegrityError
from core_apps.article.models import Article
from rest_framework.exceptions import ValidationError

class RatingCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    
    def perform_create(self, serializer):
        article_id = self.kwargs.get('article_id')
        if article_id:
            try:
                article = Article.objects.get(id=article_id)
            except Article.DoesNotExist:
                raise ValidationError("Invalid article_id provided")
        
        else:
            raise ValidationError("Article id not found")
        
        try:
            print(type(article))
            serializer.save(user=self.request.user, article=article)

        except IntegrityError:
            raise AlreadyHaveRating