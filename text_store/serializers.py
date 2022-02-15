import logging
from rest_framework import serializers
# from rest_framework.validators import UniqueValidator
# from django.contrib.contenttypes.models import ContentType
from bs4 import BeautifulSoup
import bleach
from django.utils.translation import get_language

from search_service.serializers import (
    BaseModelToIndexableSerializer,
)

from search_service.models import ResourceRelationship
import dateutil

from .models import (
    TextResource,
)

logger = logging.getLogger(__name__)

default_lang = get_language()


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
            "language",
            "creator"
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


class CreatorToIndexableSerializer(BaseModelToIndexableSerializer):
    def _date_indexable(
        self,
        type,
        subtype,
        value,
    ):
        try:
            parsed_date = dateutil.parser.parse(value)
        except ValueError:
            parsed_date = None
        if parsed_date:
            return {
                "type": type,
                "subtype": subtype.lower(),
                "indexable_date_range_start": parsed_date,
                "indexable_date_range_end": parsed_date,
                "original_content": str({subtype: bleach.clean(value)}),
            }

    def to_indexables(self, instance):
        indexables = []
        if authors := instance.get("authors"):
            for author in authors:
                # forename_initials = [x[0] if i > 0 else x for i, x in enumerate(author.get("forenames"))]
                name = ", ".join([author.get("surname"), " ".join(author.get("forenames"))])
                logger.info(name)
                indexables.append(
                    {
                        "type": "text",
                        "subtype": "author",
                        "indexable_text": BeautifulSoup(name, "html.parser").text,
                        "original_content": str({"author": bleach.clean(name)}),
                        "language": None,
                    }
                )
        # if creation_date := instance.get("date_string"):
        #     indexables.append(self._date_indexable(
        #                             type="text",
        #                             subtype="creation_date",
        #                             value=creation_date,
        #                         ))
        # logger.info(indexables)
        return indexables


class TextResourceToIndexableSerializer(BaseModelToIndexableSerializer):
    indexable_text_fields = [
        {"key": "label", "indexable_type": "text", "index_as": "text"},
        {"key": "text_title", "indexable_type": "text", "index_as": "text"},
        {"key": "text_subtitle", "indexable_type": "text", "index_as": "text"},
    ]

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
                    if index_as == "text":
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
        indexables = [
            {
                "type": "text",
                "subtype": instance.text_type,
                "original_content": bleach.clean(instance.text_content),
                "indexable_text": BeautifulSoup(instance.text_content, "html.parser").text,
                "language": instance.language,
            },
        ]
        for field_lookup in self.indexable_text_fields:
            if field := getattr(instance, field_lookup.get("key")):
                norm_field = self._normalise_field(field)
                for field_instance in norm_field:
                    indexables.extend(
                        self._indexables_from_field(field_instance, **field_lookup)
                    )
        if creator := getattr(instance, "creator"):
            indexables.extend(CreatorToIndexableSerializer().to_indexables(instance=creator))
        return indexables
