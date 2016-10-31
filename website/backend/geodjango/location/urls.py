from django.conf.urls import url, include
from location import views
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='Food Bank API')

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'location', views.LocationViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router
# We include the login URLs for the browsable API
urlpatterns = [
    url('^schema/$', schema_view),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
