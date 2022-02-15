import logging

from django.contrib.gis.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from search_service.models import (
        BaseSearchResource, 
        )

from .settings import text_store_settings

logger = logging.getLogger(__name__)


class TextResource(BaseSearchResource):
    """
    Model for storing textual resources
    """
    text_type = models.CharField(max_length=30)  # transcript, translation, etc.
    text_profile = models.URLField(blank=True, null=True)  # e.g. http://example.org/foo-transcript
    text_format = models.CharField(max_length=255)  # e.g. application/xml or application/json+ld
    # Label, text_title and text_subtitle are language maps, not strings
    label = models.JSONField(blank=True, null=True)  # Smith's Translation of the Aeneid (1836)
    text_title = models.JSONField(blank=True, null=True)  # The Aeneid: Book 1
    text_subtitle = models.JSONField(blank=True, null=True)  # Storm and Refuge
    # Assumption here that this is plaintext, markdown or HTML ?
    text_content = models.TextField(blank=True, null=True)  # Content
    selector = models.JSONField(blank=True, null=True)
    language = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        indexes = [
                models.Index(fields=["text_type"]),
                models.Index(fields=["text_profile"]),
                models.Index(fields=["text_format"]),
                models.Index(fields=["text_title"]),
                models.Index(fields=["text_subtitle"]),
                models.Index(fields=["label"]),
                models.Index(fields=["language"]),
        ]
