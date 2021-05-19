from rest_framework_extensions.routers import ExtendedSimpleRouter

from formidable.api import (
    FormApi,
    ApplicationApi,
    SectionApi,
    NestedResponseApi,
)

router = ExtendedSimpleRouter()
router.register("forms", FormApi)
router.register("sections", SectionApi).register(
    "responses",
    NestedResponseApi,
    basename="sections-responses",
    parents_query_lookups=["field__section"],
)
router.register("applications", ApplicationApi)

common_urls = router.urls
