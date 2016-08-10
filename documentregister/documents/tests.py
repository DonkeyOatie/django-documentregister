from django.test import TestCase
from django.core.urlresolvers import reverse
from documents.models import DocumentType, Document
from documents.forms import DocumentRegistrationForm
from django_webtest import WebTest


class DocumentModelTest(TestCase):

    def setUp(self):
        self.dt = DocumentType.objects.create(
            document_type_short='TST',
            document_type_long='Test Document',
            description='test description'
        )

        self.d = Document.objects.create(
            document_type=self.dt,
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

    def test_full_title(self):
        document = Document.objects.get(pk=self.d.pk)
        full_title = '{} {}'.format(
            self.d.document_type.document_type_short + str(self.d.pk).zfill(5),
            self.d.title
        )
        self.assertEqual(
            document.full_title,
            full_title
        )

    def test_document_type_str(self):
        document_type = DocumentType.objects.get(pk=self.dt.pk)
        self.assertEqual(
            str(document_type),
            '{} - {}'.format(self.dt.document_type_short, self.dt.document_type_long)
        )


class DocumentRegistrationFormTest(TestCase):

    def setUp(self):
        self.dt = DocumentType.objects.create(
            document_type_short='TST',
            document_type_long='Test Document',
            description='test description'
        )

    def test_valid_data(self):
        form = DocumentRegistrationForm({
            'title': 'Test Document',
            'document_type': self.dt.pk,
            'description': 'test document description',
            'author_name': 'Mr QA',
            'author_email': 'mr.qa@example.com',
            'link': 'https://example.com'
        })
        self.assertTrue(form.is_valid())
        document = form.save()
        self.assertEqual(document.title, 'Test Document')
        self.assertEqual(document.document_type.pk, self.dt.pk)
        self.assertEqual(document.description, 'test document description')
        self.assertEqual(document.author_name, 'Mr QA')
        self.assertEqual(document.author_email, 'mr.qa@example.com')
        self.assertEqual(document.link, 'https://example.com')

    def test_missing_data(self):
        form = DocumentRegistrationForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'title': ['This field is required.'],
            'document_type': ['This field is required.'],
            'description': ['This field is required.'],
            'author_name': ['This field is required.'],
            'author_email': ['This field is required.'],
            'link': ['This field is required.']
        })

    def test_invalid_link(self):
        form = DocumentRegistrationForm({
            'title': 'Test Document',
            'document_type': self.dt.pk,
            'description': 'test document description',
            'author_name': 'Mr QA',
            'author_email': 'mr.qa@example.com',
            'link': 'invalid_link'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'link': ['Enter a valid URL.'],
        })

    def test_invalid_email(self):
        form = DocumentRegistrationForm({
            'title': 'Test Document',
            'document_type': self.dt.pk,
            'description': 'test document description',
            'author_name': 'Mr QA',
            'author_email': 'invalid_example.com',
            'link': 'https://example.com'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'author_email': ['Enter a valid email address.'],
        })


class DocumentRegisterViewTest(WebTest):

    def setUp(self):
        self.dt = DocumentType.objects.create(
            document_type_short='TST',
            document_type_long='Test Document',
            description='test description'
        )

    def test_view_page(self):
        page = self.app.get(reverse('register'), user='Test')
        self.assertEqual(len(page.forms), 3)

    def test_submit_form(self):
        page = self.app.get(reverse('register'), user='Test')
        form = page.forms.get('register_form')
        form['title'] = 'Test'
        form['document_type'] = self.dt.pk
        form['description'] = 'test document description'
        form['author_name'] = 'Mr QA'
        form['author_email'] = 'mr.qa@example.com'
        form['link'] = 'https://example.com'
        response = form.submit()
        self.assertEqual(response.status_code, 302)
        self.assertContains(response.follow(), 'test document description')


class DocumentSearchViewTest(WebTest):

    def setUp(self):
        self.dt = DocumentType.objects.create(
            document_type_short='TST',
            document_type_long='Test Document',
            description='test description'
        )

        self.d = Document.objects.create(
            document_type=self.dt,
            title='test',
            description='test',
            author_name='Mr QA',
            author_email='qa@example.com',
            link='https://www.example.com'
        )

    def test_search_page_noresults(self):
        page = self.app.get(reverse('search') + '?q=not_going_to_find_this', user='Test')
        self.assertContains(page, 'No documents found!!! :(')

    def test_search_page_oneresult(self):
        page = self.app.get(reverse('search') + '?q=Test', user='Test')
        self.assertContains(page, self.d.tag)

    def test_search_page_noquery(self):
        page = self.app.get(reverse('search'), user='Test')
        self.assertContains(page, self.d.tag)


class DocumentDetailViewTest(WebTest):

    def setUp(self):
        self.dt = DocumentType.objects.create(
            document_type_short='TST',
            document_type_long='Test Document',
            description='test description'
        )

        self.d = Document.objects.create(
            document_type=self.dt,
            title='test',
            description='test',
            author_name='Mr QA',
            author_email='qa@example.com',
            link='https://www.example.com'
        )

    def test_detail_page(self):
        page = self.app.get(reverse('detail', kwargs={'pk': self.d.pk}), user='Test')
        self.assertContains(page, self.d.full_title)

class DocumentEditViewTest(WebTest):

    def setUp(self):
        self.dt = DocumentType.objects.create(
            document_type_short='TST',
            document_type_long='Test Document',
            description='test description'
        )

        self.d = Document.objects.create(
            document_type=self.dt,
            title='test',
            description='test',
            author_name='Mr QA',
            author_email='qa@example.com',
            link='https://www.example.com'
        )

    def test_view_edit_page(self):
        page = self.app.get(reverse('edit', kwargs={'pk': self.d.pk}), user='Test')
        self.assertEqual(len(page.forms), 3)
        form = page.forms.get('register_form')
        form['title'] = 'New Title'
        response = form.submit()
        self.assertEqual(response.status_code, 302)
        self.assertContains(response.follow(), 'New Title')
        new_d = Document.objects.get(pk=self.d.pk)
        self.assertEqual(new_d.title, 'New Title')
