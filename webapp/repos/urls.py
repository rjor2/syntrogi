from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^$', views.repo_list),
    url(r'(?P<id>.+)/$', views.repo_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)