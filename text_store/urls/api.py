from rest_framework import routers
from ..views import (
    TextResourceViewSet, TextResourceSearchViewSet
)

app_name = "text_store"

router = routers.DefaultRouter(trailing_slash=False)
router.register("text", TextResourceViewSet)
router.register("text_search", TextResourceSearchViewSet, basename="text_search")
urlpatterns = router.urls
