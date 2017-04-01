"""courgette URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from views import ResetPasswordRequestView, PasswordResetConfirmView

from django.conf.urls import *
from django.contrib import admin

urlpatterns = [
    url(r'^backend/', include('backend.urls')),
    url(r'^admin/', admin.site.urls),
    # TODO: Check if the others are going to have a custom page for this
    # url(r'^logout/$', auth_views.logout, {'next_page': 'website/index.html'}, name='logout'),
    # url(r'^logout/$', auth_views.logout, name='logout'),
    # url('^', include(inbuilt_urls)),
    # TODO: Link password reset URL to a HTML page
    url(r'^password_reset/$', ResetPasswordRequestView.as_view(), name='password_reset'),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
