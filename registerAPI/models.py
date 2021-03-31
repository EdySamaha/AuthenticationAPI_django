from django.db import models

# Create your models here.
"""NOTE: DON'T FORGET TO MIGRATE CHANGES BEFORE TESTING/RUNNING!!!
python manage.py makemigrations
python manage.py migrate"""

class Account(models.Model):
    user_id= models.IntegerField(primary_key=True, auto_created=True, blank=True) #blank=True means field will not be required in form
    username = models.CharField(max_length=20, blank=True) #blank=True for login (not required)
    email = models.EmailField(max_length=30) #PROBLEM with unique=True: Since Register and Login are using the same Model => email.unique=True applies in Login also, meaning cannot enter an existing email, meaning cannot login
    password = models.CharField(max_length=256)

    # class Meta: #PROBLEM: making Account NOT have .objects attribute => Make it abstract class and create Register 
    #     abstract = True #to override inherited attributes in subcalsses
