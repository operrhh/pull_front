from django.db import models

class Usuario(models.Model):
    person_number = models.CharField(max_length=10)
    national_id = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    person_id_hcm = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"