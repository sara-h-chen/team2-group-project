from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^(?P<username>[[a-zA-Z0-9]+)/$', views.user_page, name='user_page'),
]
