from django.apps import AppConfig


class TextStoreConfig(AppConfig):
    name = "text_store"

    def ready(self):
        from .signals import (
            index_text_resource,
        )
