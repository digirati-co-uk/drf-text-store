from rest_framework import routers
from ..views import TextResourceAPIViewSet, TextResourceAPISearchViewSet

app_name = "text_store"

router = routers.DefaultRouter()
router.register("text_resource", TextResourceAPIViewSet)
router.register(
    "text_resource_search", TextResourceAPISearchViewSet, basename="search"
)
urlpatterns = router.urls
