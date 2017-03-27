from django.conf.urls import url
from django.contrib.auth import views as auth_views

import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^food/(?P<latitude>\d+(?:\.\d+))/(?P<longitude>\d+(?:\.\d+))/$', views.foodList),
    # url(r'^search/(?P<type>[0-4]{1})/$', views.search, name='search'),
    # url(r'^courgette/(?P<userID>[0-4]{5})/$', views.notifcation, name='notifcations')
    url(r'^user/(?P<username>[a-zA-Z0-9]+)/messages/$', views.getMessages),
    url(r'^user/(?P<username>[a-zA-Z0-9]+)/contacts/$', views.getContacts),
    url(r'^user/(?P<username>[a-zA-Z0-9]+)/messages/add/$', views.addMessage),
    url(r'^user/(?P<username>[a-zA-Z0-9]+)/$', views.findUser, name='findUser'),
    # TODO: Fix this
    url(r'^accounts/login/(?P<username>[a-zA-Z0-9]+)/(?P<password>[a-zA-Z0-9]+)/$', views.authenticate),
]
