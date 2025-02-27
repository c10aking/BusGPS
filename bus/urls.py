from django.urls import path
from . import views

urlpatterns = [
    path('bus-locations/', views.fetch_bus_locations, name='fetch_bus_locations'),
]
