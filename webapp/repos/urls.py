from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^$', views.RepoList.as_view()),
    url(r'(?P<id>.+)/$', views.RepoDetail.as_view()), # could(Should) put re for uuid here instead of .+
]

urlpatterns = format_suffix_patterns(urlpatterns)