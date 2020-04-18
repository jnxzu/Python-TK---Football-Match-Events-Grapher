from . import views
from django.urls import path

urlpatterns = [
    path('', views.landing, name='landing'),
    path('grapher', views.main, name='grapher')
]
