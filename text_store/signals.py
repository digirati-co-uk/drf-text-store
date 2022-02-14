import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import TextResource
from .tasks import TextResourceIndexingTask
from .settings import text_store_settings

logger = logging.getLogger(__name__)


@receiver(post_save, sender=TextResource)
def index_text_resource(sender, instance, **kwargs):
    if text_store_settings.INDEX_TEXT_RESOURCES:
        logger.info(f"Running the TextResourceIndexingTask for: ({instance.id})")
        task = TextResourceIndexingTask(instance.id)
        task.run()
    else:
        logger.info("Signal received but no indexing")
