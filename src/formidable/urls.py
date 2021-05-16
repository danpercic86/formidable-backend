from rest_framework_extensions.routers import ExtendedSimpleRouter

from formidable.api import (
    FormApi,
    ApplicationApi,
    SectionApi,
    ResponseApi,
)

router = ExtendedSimpleRouter()
router.register("forms", FormApi)
router.register("sections", SectionApi)
router.register("applications", ApplicationApi).register(
    "responses",
    ResponseApi,
    basename="responses",
    parents_query_lookups=["application_id"],
)

common_urls = router.urls
