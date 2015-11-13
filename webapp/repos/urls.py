from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.repo_list),
    url(r'(?P<id>.+)/$', views.repo_detail),
]