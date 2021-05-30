from typing import List

from formidable.models import Form, Section, Field
from tests.formidable.factories import FormFactory, FieldFactory, SectionFactory

for _ in range(5):
    form: Form = FormFactory.create()
    sections: List[Section] = SectionFactory.create_batch(3, form=form)
    for section in sections:
        fields: List[Field] = FieldFactory.create_batch(4, section=section)
