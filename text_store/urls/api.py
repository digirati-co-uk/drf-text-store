from rest_framework import routers
from ..views import (
    TextResourceViewSet,
)

app_name = "text_store"

router = routers.DefaultRouter(trailing_slash=False)
router.register("text", TextResourceViewSet)
urlpatterns = router.urls
