from django.db import models
from datetime import datetime

# Create your models here.
class Search(models.Model):
    search = models.CharField(max_length=300,)
    created = models.DateField(auto_now=True)

    def __str__(self):
        return self.search


    class Meta:
            verbose_name_plural = 'Searches'