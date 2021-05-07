"""dataPrivacy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from page import amazon_auth_script

"""if we make the path 'page/', the webpage will have to be /page/ to reach it
' ' means it will be the home page on startup"""
app_name = 'main'
urlpatterns = [
    path('', include(('page.urls'), namespace='home')),
    path('admin/', admin.site.urls),
    path('accounts/profile/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('accounts/', include('allauth.urls')),
    url(r'^accounts/', include('allauth.urls')),
    
    path('', amazon_auth_script.getAccessToken, name='amzn_auth_script'),
    path('', amazon_auth_script.getProfile, name='amzn_profile_script')
]
