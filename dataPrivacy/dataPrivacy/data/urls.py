# djbootstrap4/bootstrap4/urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'', views.bootstrap4_index, name="index"),
]
