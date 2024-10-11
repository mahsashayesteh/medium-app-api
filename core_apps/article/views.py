import logging
from django.http import Http404
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Article, ArticleView
from rest_framework import filters, generics, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ArticleSerializers
from .filters import ArticleFilter
from .pagination import ArticlePaginagtion
from .renderers import ArticleJSONRenderer, ArticlesJSONRenderer
from .permissions import IsOwnerOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage

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