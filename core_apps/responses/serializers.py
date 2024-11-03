from rest_framework import serializers
from .models import Response

class ResponseSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source = "user.email", 
                                       read_only = True)
    article_title = serializers.CharField(source = "article.title", 
                                          read_only = True)
    
    class Meta:
        model = Response
        fields = ["id","user_email", "article_title", "parent_response",
                 "content", "created_at"]
