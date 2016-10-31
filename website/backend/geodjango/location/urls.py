from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from location import views

urlpatterns = [
    url(r'^location/$', views.LocationList.as_view()),
    url(r'^location/(?P<pk>[0-9]+)/$', views.LocationDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
