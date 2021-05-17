import json
from pprint import pprint
from typing import List

from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from administration.models import User
from formidable.api import ApplicationApi
from formidable.models import Form, Section, Field, Validator
from tests.formidable.factories import (
    FormFactory,
    SectionFactory,
    FieldFactory,
    UserFactory,
    ValidatorFactory,
)


class FormApiTests(APITestCase):
    def setUp(self) -> None:
        FormFactory.create_batch(5)

    def test_list_returns_all_forms(self):
        response = self.client.get("/api/forms/")
        pprint(response.__dict__)
        pprint(response.data)
        self.assertEqual(response.status_code, 200)


class ApplicationsApiTests(APITestCase):
    def setUp(self) -> None:
        self.form: Form = FormFactory.create()
        pprint(self.form)
        self.section: Section = SectionFactory.create(form=self.form)
        self.fields: List[Field] = FieldFactory.create_batch(3, section=self.section)
        self.validator: Validator = ValidatorFactory.create(field=self.fields[0])
        self.user: User = UserFactory.create()
        self.client.login(username=self.user.username, password=self.user.password)

    def test_post_with_no_content_returns_error(self):
        response = self.client.post("/api/applications/")
        form_error: List[ErrorDetail] = response.data.get("form")
        responses_error: List[ErrorDetail] = response.data.get("responses")

        self.assertEqual(response.status_code, 400)

        self.assertEqual(form_error.__len__(), 1)
        self.assertEqual(str(form_error[0]), "This field is required.")
        self.assertEqual(form_error[0].code, "required")

        self.assertEqual(responses_error.__len__(), 1)
        self.assertEqual(str(responses_error[0]), "This field is required.")
        self.assertEqual(responses_error[0].code, "required")

    def test_create_application_returns_201(self):
        data = {
            "form": self.form.id,
            "responses": [
                {"value": "random value", "field": self.fields[0].id},
                {"value": "anther value", "field": self.fields[1].id},
            ],
        }
        factory = APIRequestFactory()
        request = factory.post("/api/applications/", data, format="json")
        request.data = json.dumps(data)
        force_authenticate(request, self.user)
        response = ApplicationApi.as_view({"post": "create"})(request)
        pprint(response.__dict__)
        # response = self.client.post('/api/applications/', data,
        #                             content_type='application/json')
        # pprint(response.__dict__)
        self.assertEqual(response.status_code, 201)
