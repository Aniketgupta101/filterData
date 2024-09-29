from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=15)
    contact_number = models.CharField(max_length=10)
    address = models.CharField(max_length=25)  #
    city = models.CharField(max_length=15)
    age = models.CharField(max_length=2)
    professional = models.CharField(max_length=25)
    

    def __str__(self):
        return self.username

    
