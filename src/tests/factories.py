import factory
from factory.django import DjangoModelFactory

from formidable.models import Form, Section


class FormFactory(DjangoModelFactory):
    class Meta:
        model = Form

    name = factory.Faker('name')
    description = factory.Faker('text')


class SectionFactory(DjangoModelFactory):
    class Meta:
        model = Section

    name = factory.Faker('name')
    description = factory.Faker('text')
