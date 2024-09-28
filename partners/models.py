from django.db import models

class Partner(models.Model):
    name = models.CharField(max_length=255)
    logo = models.URLField(max_length=200)  # URL to the image
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name