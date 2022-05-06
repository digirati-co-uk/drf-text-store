import logging

# Django Imports
from rest_framework import viewsets
from search_service.views import (
    BaseAPISearchViewSet,
    BasePublicSearchViewSet,
)
from search_service.parsers import (
    ResourceSearchParser,
)
from search_service.filters import (
    ResourceFilter,
    FacetFilter,
    RankSnippetFilter,
)

# Local imports
from .models import TextResource
from .serializers import (
    TextResourceAPICreateSerializer,
    TextResourceAPIListSerializer,
    TextResourceAPIDetailSerializer,
    TextResourceAPISearchSerializer,
    TextResourcePublicListSerializer,
    TextResourcePublicDetailSerializer,
    TextResourcePublicSearchSerializer,
)

# This should be replaced by an import from a utils package.
from .utils import (
    ActionBasedSerializerMixin,
)

logger = logging.getLogger(__name__)


class TextResourceAPIViewSet(ActionBasedSerializerMixin, viewsets.ModelViewSet):
    queryset = TextResource.objects.all()
    serializer_mapping = {
        "default": TextResourceAPIDetailSerializer,
        "create": TextResourceAPICreateSerializer,
        "list": TextResourceAPIListSerializer,
    }
    lookup_field = "id"


class TextResourcePublicViewSet(
    ActionBasedSerializerMixin, viewsets.ReadOnlyModelViewSet
):
    queryset = TextResource.objects.all()
    lookup_field = "id"
    serializer_mapping = {
        "default": TextResourcePublicDetailSerializer,
        "list": TextResourcePublicListSerializer,
    }


class TextResourceAPISearchViewSet(BaseAPISearchViewSet):
    """ """

    queryset = TextResource.objects.all().distinct()
    parser_classes = [ResourceSearchParser]
    filter_backends = [
        ResourceFilter,
        FacetFilter,
        RankSnippetFilter,
    ]
    serializer_class = TextResourceAPISearchSerializer


class TextResourcePublicSearchViewSet(BasePublicSearchViewSet):
    """ """

    queryset = TextResource.objects.all().distinct()
    parser_classes = [ResourceSearchParser]
    filter_backends = [
        ResourceFilter,
        FacetFilter,
        RankSnippetFilter,
    ]
    serializer_class = TextResourcePublicSearchSerializer
