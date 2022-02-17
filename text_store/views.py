import logging

# Django Imports
from rest_framework import viewsets
from search_service.views import JSONResourceSearchViewSet

# Local imports
from .models import TextResource
from .serializers import (
    TextResourceCreateSerializer,
    TextResourceSummarySerializer,
    TextSearchSerializer
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


class TextResourceSearchViewSet(JSONResourceSearchViewSet):
    """ """
    queryset = TextResource.objects.all().distinct()
    serializer_class = TextSearchSerializer
