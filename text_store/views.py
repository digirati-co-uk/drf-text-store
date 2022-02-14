import logging

# Django Imports
from rest_framework import viewsets
from rest_framework.decorators import action

from rest_framework.response import Response

# Local imports
from .models import TextResource
from .serializers import (
    TextResourceCreateSerializer,
    TextSerializer,
    TextResourceSummarySerializer,
)

# This should be replaced by an import from a utils package.
from .utils import (
    ActionBasedSerializerMixin,
)

logger = logging.getLogger(__name__)


class TextResourceViewSet(ActionBasedSerializerMixin, viewsets.ModelViewSet):
    queryset = TextResource.objects.all()
    serializer_mapping = {
        "default": TextResourceCreateSerializer,
        "create": TextResourceCreateSerializer,
        "list": TextResourceSummarySerializer,
    }
    lookup_field = "id"


class TextResourcePublicViewSet(ActionBasedSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = TextResource.objects.all()
    lookup_field = "id"
    serializer_mapping = {
        "default": TextResourceCreateSerializer,
        "create": TextResourceCreateSerializer,
        "list": TextResourceSummarySerializer,
    }
    # serializer_class = TextResourceCreateSerializer
