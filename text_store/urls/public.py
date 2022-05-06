from rest_framework import routers
from text_store.views import (
    TextResourcePublicViewSet,
    TextResourcePublicSearchViewSet,
)

app_name = "text_store"

router = routers.SimpleRouter()
router.register("text", TextResourcePublicViewSet)
router.register("search", TextResourcePublicSearchViewSet, basename="search")
urlpatterns = router.urls
