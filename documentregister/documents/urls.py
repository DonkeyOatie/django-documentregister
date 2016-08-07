from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from documents import views

urlpatterns = [
    url(r'^$', login_required(views.DocumentRegistrationView.as_view()), name='register'),
    url(r'^document/(?P<pk>[^/]+)$', login_required(views.DocumentDetailView.as_view()), name='detail'),
    url(r'^edit/(?P<pk>[^/]+)$', login_required(views.DocumentEditView.as_view()), name='edit'),
    url(r'^search$', login_required(views.DocumentSearchView.as_view()), name='search')
]
