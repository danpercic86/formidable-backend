from pprint import pprint
from typing import List

from django.urls import path, include, reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase, URLPatternsTestCase

import formidable.urls
from administration.models import User
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


class ApplicationsApiTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("api/", include(formidable.urls.common_urls))]

    list_url = reverse("application-list")

    def setUp(self) -> None:
        self.form: Form = FormFactory.create()
        self.section: Section = SectionFactory.create(form=self.form)
        self.fields: List[Field] = FieldFactory.create_batch(3, section=self.section)
        self.validator: Validator = ValidatorFactory.create(field=self.fields[0])
        self.user: User = UserFactory.create()
        self.client.force_authenticate(user=self.user)

    def test_post_with_no_content_returns_error(self):
        response = self.client.post(self.list_url)
        form_error: List[ErrorDetail] = response.data.get("form")
        responses_error: List[ErrorDetail] = response.data.get("responses")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(form_error.__len__(), 1)
        self.assertEqual(str(form_error[0]), "This field is required.")
        self.assertEqual(form_error[0].code, "required")

        self.assertEqual(responses_error.__len__(), 1)
        self.assertEqual(str(responses_error[0]), "This field is required.")
        self.assertEqual(responses_error[0].code, "required")

    def test_authentication_is_required(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.list_url, {})
        detail: ErrorDetail = response.data.get("detail")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(detail), "Authentication credentials were not provided.")
        self.assertEqual(detail.code, "not_authenticated")

    def test_create_application_returns_201(self):
        data = {
            "form": self.form.id,
            "responses": [
                {"value": "random value with longer name", "field": self.fields[0].id},
                {"value": "anther value", "field": self.fields[1].id},
            ],
        }

        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
