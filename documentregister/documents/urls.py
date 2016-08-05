from django.conf.urls import url
from documents import views

urlpatterns = [
    url(r'^$', views.DocumentRegistrationView.as_view(), name='register'),
    url(r'^document/(?P<pk>[^/]+)$', views.DocumentDetailView.as_view(), name='detail')
]
