from rest_framework import serializers
from .models import Rating

class RatingSerializer(serializers.ModelSerializer):
    article_title = serializers.CharField(source= "article.title", 
                                          read_only=True)
    user_email = serializers.CharField(source="user.email", 
                                       read_only=True)
    
    class Meta:
        model = Rating
        fields = [
            "id", "article_title", "user_email", "value", "review"
        ]
    
