from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import ArticleDocument

class ArticleElasticSearchSerializer(DocumentSerializer):
    
    class Meta:
        document = ArticleDocument
        fields = ["title", "description", "author", "slug", "body", 
                  "created_at"]
