from django.test import TestCase
from documents.models import DocumentType, Document


class DocumentModelTest(TestCase):

    def setUp(self):
        dt = DocumentType.objects.create(
            document_type_short='TST',
            document_type_long='Test Document',
            description='test description'
        )

        self.d = Document.objects.create(
            document_type=dt,
            title='test',
            description='test',
            author_name='Mr QA',
            author_email='qa@example.com',
            link='https://www.example.com'
        )

    def test_document_tag(self):
        document = Document.objects.get(pk=self.d.pk)
        self.assertEqual(
            document.tag,
            self.d.document_type.document_type_short + str(self.d.pk).zfill(5)
        )
