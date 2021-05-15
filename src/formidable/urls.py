from rest_framework_extensions.routers import ExtendedSimpleRouter

from formidable.views import (
    FormViewSet,
    ApplicationViewSet,
    FormSectionViewSet,
    ResponseViewSet,
)

router = ExtendedSimpleRouter()
router.register("forms", FormViewSet)
router.register("sections", FormSectionViewSet)
router.register("applications", ApplicationViewSet).register(
    "responses",
    ResponseViewSet,
    basename="responses",
    parents_query_lookups=["application_id"],
)

common_urls = router.urls
