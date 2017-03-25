from django.conf.urls import url
from django.contrib.auth import views as auth_views

import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^food/(?P<location>[a-zA-Z]+)/$', views.foodList),
    # url(r'^search/(?P<type>[0-4]{1})/$', views.search, name='search'),
    # url(r'^courgette/(?P<userID>[0-4]{5})/$', views.notifcation, name='notifcations')
    url(r'^user/(?P<username>[a-zA-Z0-9]+)/messages$', views.getMessages),
    url(r'^user/(?P<username>[a-zA-Z0-9]+)/$', views.findUser, name='findUser'),
    url(r'^accounts/login/(?P<username>[a-zA-Z0-9]+)/(?P<password>[a-zA-Z0-9]+)/$', views.authenticate),
]
