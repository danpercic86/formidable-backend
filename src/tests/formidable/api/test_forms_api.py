from pprint import pprint

from rest_framework.test import APITestCase

from tests.formidable.factories import FormFactory


class FormApiTests(APITestCase):
    def setUp(self) -> None:
        self.forms = FormFactory.create_batch(5)

    def test_list_returns_all_forms(self):
        response = self.client.get("/api/forms/")
        pprint(response.__dict__)
        pprint(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
