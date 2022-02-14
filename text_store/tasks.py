import logging

from search_service.tasks import BaseSearchServiceIndexingTask

from .models import TextResource

from .serializers import (
    TextResourceToIndexableSerializer,
)


class TextResourceIndexingTask(BaseSearchServiceIndexingTask):
    model = TextResource
    serializer_class = TextResourceToIndexableSerializer
