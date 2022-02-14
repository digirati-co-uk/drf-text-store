from django.urls import path, include
from rest_framework import routers

app_name = 'api'
router = routers.DefaultRouter(trailing_slash=False)
include_urls = [
    path("text_store/", include(("text_store.urls.api"))),
    path("text_store/", include(("text_store.urls"))),
]
urlpatterns = router.urls + include_urls
