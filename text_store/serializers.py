import logging
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.contenttypes.models import ContentType
from bs4 import BeautifulSoup
import bleach

from search_service.serializers import (
    BaseModelToIndexableSerializer,
)

from search_service.models import ResourceRelationship

from .models import (
    TextResource,
)

logger = logging.getLogger(__name__)


class TextResourceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextResource
        fields = [
            "id",
            "text_type",
            "text_profile",
            "text_format",
            "label",
            "text_title",
            "text_subtitle",
            "text_content",
            "selector",
            "language"
        ]


class TextSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return instance.text_content

    class Meta:
        model = TextResource
        fields = ["text_content"]


class TextResourceSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TextResource
        fields = [
            "url",
            "label",
            "text_title",
            "text_subtitle",
        ]
        extra_kwargs = {
            "url": {
                "view_name": "text_store:textresource-detail",
                "lookup_field": "id",
            }
        }


class LanguageMapToIndexablesSerializer(BaseModelToIndexableSerializer):
    """
    Sample:

    ```
    {
      "label": {
        "en": [
          "Whistler's Mother",
          "Arrangement in Grey and Black No. 1: The Artist's Mother"
        ],
        "fr": [
          "Arrangement en gris et noir no 1",
          "Portrait de la mère de l'artiste",
          "La Mère de Whistler"
        ],
        "none": [ "Whistler (1871)" ]
      }
    }
    ```
    Output:

    [
        {
        "type": ?, "subtype": "label". "original_content":
        }
    ]
    """

    def to_indexables(self, instance):
        return []


class TextResourceToIndexableSerializer(BaseModelToIndexableSerializer):
    def to_indexables(self, instance):
        return [
            {
                "type": "text",
                "subtype": instance.text_type,
                "original_content": bleach.clean(instance.text_content),
                "indexable_text": BeautifulSoup(instance.text_content, "html.parser").text,
                "language": instance.language,
            }
        ]
