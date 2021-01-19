from rest_framework.routers import DefaultRouter

from formidable.views import FormViewSet, ResponseViewSet

router = DefaultRouter()
router.register("forms", FormViewSet)
router.register("responses", ResponseViewSet)

common_urls = router.urls
