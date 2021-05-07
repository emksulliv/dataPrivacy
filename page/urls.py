from django.urls import path
from . import views
from django.conf.urls import url


from . import views
app_name = 'page'
urlpatterns = [
    path('', views.index, name='index'),
    path('', views.login, name='login'),
]
