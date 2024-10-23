from rest_framework import serializers
from .models import Article, ArticleView, Clap
from core_apps.profiles.serializers import ProfileSerializers
from core_apps.bookmarks.models import BookMarks
from core_apps.bookmarks.serializers import BookMarkSerializer

class TagListField(serializers.Field):
    def to_representation(self, value):
        return [tag.name for tag in value.all()]
    
    def to_internal_value(self, data):
        if not isinstance(data, list):
            raise serializers.ValidationError("باید لیستی از برچسب ها باشد")
        tag_objects = []
        for tag_name in data:
            tag_name = tag_name.strip()

            if not tag_name:
                continue
            tag_objects.append(tag_name)
        return tag_objects
    
class ArticleSerializers(serializers.ModelSerializer):
    author_info = ProfileSerializers(source = "author.profile", read_only=True)
    banner_image = serializers.SerializerMethodField()
    average_rating = serializers.ReadOnlyField()
    article_read_time = serializers.ReadOnlyField()
    tags = TagListField()
    view = serializers.SerializerMethodField()
    bookmark = serializers.SerializerMethodField()
    bookmark_count = serializers.SerializerMethodField()
    claps_count = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    
    def get_bookmark(self, obj):
        try:
           bookmark = BookMarks.objects.filter(article=obj)
           return BookMarkSerializer(bookmark, many=True).data
        except BookMarks.DoesNotExist:
            bookmark = None
            return bookmark
    
    def get_bookmark_count(self, obj):
        return BookMarks.objects.filter(article=obj).count()
    
    def get_claps_count(self, obj):
        return obj.claps.count()

    def get_view(self, obj):
        return ArticleView.objects.filter(article=obj).count()
    
    def get_average_rating(self, obj):
        obj.average_rating()

    def get_banner_image(self, obj):
        return obj.banner_image.url
    
    def get_created_at(self, obj):
        now = obj.created_at
        formated_date = now.strftime("%m/%d/%Y , %H:%M:%S")
        return formated_date
    
    def get_updated_at(self, obj):
        then = obj.updated_at
        formated_date = then.strftime("%m/%d/%Y , %H:%M:%S")
        return formated_date
    
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        article = Article.objects.create(**validated_data)
        article.tags.set(tags)
        return article
    
    def update(self, instance, validated_data):
        instance.author = validated_data.get("author", instance.author)
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.body = validated_data.get("body", instance.body)
        
        if "tags" in validated_data:
            instance.tags.set(validated_data["tags"])
        instance.save()
        return instance
    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "slug",
            "tags",
            "view",
            "article_read_time",
            "author_info",
            "description",
            "body",
            "banner_image",
            "average_rating",
            "bookmark",
            "bookmark_count",
            "claps_count",
            "created_at",
            "updated_at",
        )

class ClapSerializer(serializers.ModelSerializer):
    article_title = serializers.CharField(source="Article.title", read_only=True)
    user_email = serializers.CharField(source="User.email", read_only=True)

    class Meta:
        model = Clap
        field = [
            "id", "article_title", "user_email", 
        ]