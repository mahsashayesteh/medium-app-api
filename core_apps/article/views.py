import logging
from django.http import Http404
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Article, ArticleView, Clap
from rest_framework import filters, generics, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ArticleSerializers, ClapSerializer
from .filters import ArticleFilter
from .pagination import ArticlePaginagtion
from .renderers import ArticleJSONRenderer, ArticlesJSONRenderer
from .permissions import IsOwnerOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
from django.db import transaction

user = get_user_model()

logger = logging.getLogger(__name__)

class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializers
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticated]
    pagination_class = ArticlePaginagtion
    filter_backends = (
        DjangoFilterBackend, filters.OrderingFilter,
    )
    filterset_class = ArticleFilter
    renderer_classes = [ArticlesJSONRenderer]
    ordering_fields = ["created_at", "updated_at"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        logger.info(f"article {serializer.data.get('title')} created by{self.request.user.email}")
    
class ArticleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
        permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        queryset = Article.objects.all()
        renderer_classes = [ArticleJSONRenderer]
        serializer_class = ArticleSerializers
        lookup_field = "id"
        parser_classes = [MultiPartParser, FormParser]

        def perform_update(self, serializer):
            instance = serializer.save(author=self.request.user)
            print(instance)
            print(self.request.FILES)
            if "banner_image" in self.request.FILES:
                 if instance.banner_image and instance.banner_image.name != "/profile_defaul.png":
                      default_storage.delete(instance.banner_image.path)
                 instance.banner_image = self.request.FILES["banner_image"]
                 instance.save()
        
        def retrieve(self, request, *args, **kwargs):
            try:
                instance = self.get_object()
            except:
                 return Response(status= status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(instance)
            viewer_ip = request.META.get('REMOTE_ADDR', None)
            ArticleView.record_view(
                 article=instance, user= request.user, viewer_ip=viewer_ip
            )
            return Response(serializer.data)

class ClapView(generics.CreateAPIView, generics.DestroyAPIView):
     queryset = Clap.objects.all()
     serializer_class = ClapSerializer
     lookup_field = "id"

     def create(self, request, *args, **kwargs):
          article_id = kwargs.get("article_id")
          user = request.user
          article = get_object_or_404(Article, id=article_id)

          if Clap.objects.filter(article=article, user=user).exists():
               return Response(
                    {"detail":"You have already clapped this article"},
                    status=status.HTTP_400_BAD_REQUEST
               )
          clap = Clap.objects.create(article = article, user=user)
          clap.save()
          return Response(
               {"detail":"You clapped this article"},
               status=status.HTTP_201_CREATED
          )
     
     def delete(self, request, *args, **kwargs):
          user = request.user
          article_id = kwargs.get("article_id")
          article = Article.objects.filter(id=article_id).first()
          if not article :
              return Response(
               {"detail":'invalid article id'},
               status=status.HTTP_404_NOT_FOUND
                )
          
          
          clap = get_object_or_404(Clap, user=user, article=article)
          try:
               clap.delete()
               return Response(
                    {"detail": "clap removed from article"},
                    status=status.HTTP_204_NO_CONTENT
               )
          except Exception as e:
               # لاگ کردن خطا برای بررسی
               logger.error(f"Error occurred during delete: {str(e)}")
               return Response(
                    {"detail": f"An error occurred: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
               )
     