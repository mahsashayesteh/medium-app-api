from rest_framework import serializers
from .models import BookMarks

class BookMarkSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", 
                                 read_only=True)
    article_title = serializers.CharField(source="article.title",
                                    read_only=True)
    
    class Meta:
        model = BookMarks
        fields = [
            "id", "user_email", "article_title", "created_at"
        ]
        read_only_fields = ["user_email"]

