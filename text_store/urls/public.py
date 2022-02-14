from rest_framework import routers
from text_store.views import (
    TextResourcePublicViewSet,
)

app_name = "text_store"

router = routers.SimpleRouter()
router.register("text", TextResourcePublicViewSet)
urlpatterns = router.urls
