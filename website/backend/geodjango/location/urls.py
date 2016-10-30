from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from location import views

urlpatterns = [
    url(r'^location/$', views.location_list),
    url(r'^location/(?P<pk>[0-9]+)/$', views.location_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
