import logging
from rest_framework import serializers

# from rest_framework.validators import UniqueValidator
# from django.contrib.contenttypes.models import ContentType
from bs4 import BeautifulSoup
import bleach
from django.utils.translation import get_language

from search_service.serializers.indexing import BaseModelToIndexableSerializer
from search_service.serializers.search import BaseRankSnippetSearchSerializer


from search_service.models import ResourceRelationship

from .models import (
    TextResource,
)

logger = logging.getLogger(__name__)

default_lang = get_language()


class TextResourceAPICreateSerializer(serializers.ModelSerializer):
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
            "source_language",
            "target_language",
            "people",
        ]


class TextResourceAPIDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return instance.text_content

    class Meta:
        model = TextResource
        fields = ["text_content"]


class TextResourceAPIListSerializer(serializers.HyperlinkedModelSerializer):
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
                "view_name": "api:text_store:textresource-detail",
                "lookup_field": "id",
            }
        }


class TextResourceAPISearchSerializer(BaseRankSnippetSearchSerializer):
    class Meta:
        model = TextResource
        fields = [
            "id",
            "created",
            "modified",
            "label",
            "text_title",
            "text_subtitle",
            "rank",
            "snippet",
        ]
        extra_kwargs = {
            "url": {
                "view_name": "api:text_store:textresource-detail",
                "lookup_field": "id",
            }
        }


class TextResourcePublicListSerializer(serializers.HyperlinkedModelSerializer):
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
                "view_name": "api:text_store:textresource-detail",
                "lookup_field": "id",
            }
        }


class TextResourcePublicDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return instance.text_content

    class Meta:
        model = TextResource
        fields = ["text_content"]


class TextResourcePublicSearchSerializer(BaseRankSnippetSearchSerializer):
    class Meta:
        model = TextResource
        fields = [
            "id",
            "created",
            "modified",
            "label",
            "text_title",
            "text_subtitle",
            "rank",
            "snippet",
        ]
        extra_kwargs = {
            "url": {
                "view_name": "api:text_store:textresource-detail",
                "lookup_field": "id",
            }
        }


class TextResourceToIndexableSerializer(BaseModelToIndexableSerializer):
    indexable_text_fields = [
        {"key": "label", "indexable_type": "text", "index_as": "text"},
        {"key": "text_title", "indexable_type": "text", "index_as": "text"},
        {"key": "text_subtitle", "indexable_type": "text", "index_as": "text"},
        # {"key": "people", "indexable_type": "text", "index_as": "person"},
    ]

    def _person_indexable(
        self,
        type,
        subtype,
        value,
        language,
    ):
        """
        Placeholder at the moment.
        :param type:
        :param subtype:
        :param value:
        :param language:
        :return:
        """
        return {
            "type": type,
            "subtype": subtype.lower(),
            "indexable_text": BeautifulSoup(
                ", ".join([value.get("surname"), " ".join(value.get("forenames"))]),
                "html.parser",
            ).text,
            "original_content": str(
                {
                    "creator": bleach.clean(
                        ", ".join(
                            [value.get("surname"), " ".join(value.get("forenames"))]
                        )
                    )
                }
            ),
            "language": language,
        }

    def _text_indexable(
        self,
        type,
        subtype,
        value,
        language,
    ):
        return {
            "type": type,
            "subtype": subtype.lower(),
            "indexable_text": BeautifulSoup(value, "html.parser").text,
            "original_content": str({subtype: bleach.clean(value)}),
            "language": language,
        }

    def _normalise_field(self, field_data):
        if isinstance(field_data, dict):
            return [field_data]
        elif isinstance(field_data, list):
            return field_data
        else:
            return [{"none": field_data}]

    def _normalise_language(self, language):
        if language in ["@none", "none"]:
            return default_lang
        else:
            return language

    def _indexables_from_field(
        self,
        field_instance,
        key=None,
        indexable_type="descriptive",
        index_as="text",
    ):
        indexables = []
        for val_lang, vals in field_instance.items():
            lang = self._normalise_language(val_lang)
            if vals:
                for str_value in map(str, vals):
                    if index_as == "text" and str_value.strip():
                        indexables.append(
                            self._text_indexable(
                                type=indexable_type,
                                subtype=key,
                                value=str_value,
                                language=lang,
                            )
                        )
        return indexables

    def to_indexables(self, instance):
        if hasattr(instance, "target_language"):
            text_language = instance.target_language
        elif hasattr(instance, "source_language"):
            text_language = instance.source_language
        else:
            text_language = None
        indexables = [
            {
                "type": "text",
                "subtype": instance.text_type,
                "original_content": bleach.clean(instance.text_content),
                "indexable_text": BeautifulSoup(
                    instance.text_content, "html.parser"
                ).text,
                "language": text_language,
            },
        ]
        for field_lookup in self.indexable_text_fields:
            if field := getattr(instance, field_lookup.get("key")):
                norm_field = self._normalise_field(field)
                for field_instance in norm_field:
                    indexables.extend(
                        self._indexables_from_field(field_instance, **field_lookup)
                    )
        return indexables
