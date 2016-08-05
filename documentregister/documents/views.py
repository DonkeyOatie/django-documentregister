from django.views.generic.edit import FormView, CreateView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse

from documents.models import Document

from documents.forms import DocumentRegistrationForm


class DocumentRegistrationView(CreateView):
    template_name = 'register.html'
    form_class = DocumentRegistrationForm
    model = Document

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.pk})


class DocumentDetailView(DetailView):
    template_name = 'detail.html'
    model = Document
