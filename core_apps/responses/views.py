from .models import Response, Article
from rest_framework import generics
from .serializers import ResponseSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions
from rest_framework.generics import get_object_or_404

class ResponseListCreateView(generics.ListCreateAPIView):
    queryset = Response.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResponseSerializer

    def get_queryset(self):
        article_id = self.kwargs.get("article_id")
        article = Article.objects.get(id=article_id)
        return Response.objects.filter(article=article, 
                                       parent_response=None)
    def perform_create(self, serializer):
        article_id = self.kwargs.get("article_id")
        article = get_object_or_404(Article, id=article_id)
        user = self.request.user
        serializer.save(user=user, article=article)

class ResponseUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    lookup_field = "id"

    def perform_update(self, serializer):
        user = self.request.user
        response = self.get_object()
        if user != response.user:
            raise PermissionDenied("you don't have permission to edit this response")
        serializer.save()
    def perform_destroy(self, instance):
        user = self.request.user
        response = self.get_object()
        if user != response.user :
            raise PermissionDenied("you can not delete this response")
        instance.delete()
           