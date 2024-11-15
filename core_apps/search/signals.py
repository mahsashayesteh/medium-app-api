from django_elasticsearch_dsl.registries import registry
from django.dispatch import receiver
from core_apps.article.models import Article
from django.db.models.signals import post_delete, post_save

@receiver(post_save, sender=Article)
def update_document(sender, created=False, instance=None, **kwargs):
    registry.update(instance)

@receiver(post_delete, sender=Article)
def delete_document(sender, instance=None, **kwargs):
    registry.delete(instance)