from . import views
from django.urls import path

urlpatterns = [
    path('', views.landing, name='landing'),
    path('grapher', views.main, name='grapher'),
    path('getSeasons', views.get_seasons, name='getSeasons'),
    path('getMatches', views.get_matches, name='getMatches')
]
