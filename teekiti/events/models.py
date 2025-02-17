from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    location = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='images/', blank=True, null=True)  # New field
    google_map_link = models.URLField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per ticket
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} at {self.venue}"
    

class Conference(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    location = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='images/', blank=True, null=True)  # New field
    google_map_link = models.URLField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per ticket
    description = models.TextField(blank=True)


    def __str__(self):
        return f"{self.name} at {self.venue}"
 