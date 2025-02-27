from django.db import models

# Create your models here.
from django.db import models

class Bus(models.Model):
    bus_id = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    route_id = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.vehicle_number} ({self.bus_id})"