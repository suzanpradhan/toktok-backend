from django.db import models

class Image(models.Model):
    image_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')

