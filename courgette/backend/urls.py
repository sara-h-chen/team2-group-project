from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^food/$', views.food_list),
    # url(r'^search/(?P<type>[0-4]{1})/$', views.search, name='search'),
    # url(r'^courgette/(?P<userID>[0-4]{5})/$', views.notifcation, name='notifcations')
    # url(r'^(?P<username>[[a-zA-Z0-9]+)/$', views.user_page, name='user_page'),
]
