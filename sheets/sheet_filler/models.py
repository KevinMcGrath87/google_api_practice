from django.db import models

# Create your models here.

class Cell(models.Model):
    cell_address = models.CharField(max_length=2)
    cell_value = models.TextField
    