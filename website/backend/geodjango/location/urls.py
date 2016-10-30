from django.conf.urls import url
from location import views

urlpatterns = [
    url(r'^location/$', views.location_list),
    url(r'^location/(?P<pk>[0-9]+)/$', views.location_detail),
]
