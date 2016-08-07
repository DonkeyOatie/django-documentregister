from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

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


class DocumentEditView(UpdateView):
    template_name = 'register.html'
    form_class = DocumentRegistrationForm
    model = Document

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.pk})


class DocumentSearchView(ListView):
    template_name = 'search.html'
    model = Document
    paginate_by = 25

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            vector = SearchVector('title', 'description', 'author_name', 'author_email')
            query = SearchQuery(self.request.GET.get('q'))
            object_list = Document.objects.annotate(
                rank=SearchRank(vector, query),
                search=vector
            ).filter(search=query).order_by('-rank')
        else:
            object_list = Document.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        ctx = super(DocumentSearchView, self).get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', "")
        return ctx
