from django.db import models

class Work (models.Model):
    PersonId = models.IntegerField()
    PersonNumber = models.CharField(max_length=20)
    FirstName = models.CharField(max_length=25)
    LastName = models.CharField(max_length=25)
    
