from django.db import models

class Persona(models.Model):
    id_job = models.IntegerField ()
    person_number = models.CharField(max_length=10)
    national_id = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    person_id_hcm = models.CharField(max_length=15)
    location = models.CharField(max_length= 15)
    bussines_unit = models.CharField(max_length= 20)
    department = models.CharField(max_length= 15)
    assignment_category = models.CharField(max_length= 20)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
      