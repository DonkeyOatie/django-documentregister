from django.forms import ModelForm
from documents.models import Document


class DocumentRegistrationForm(ModelForm):

    class Meta:
        model = Document
        fields = ['title', 'document_type', 'description', 'author_name', 'author_email', 'link']
