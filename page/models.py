from django.db import models

# Create your models here.
class User(models.Model):
    session_id = models.CharField(max_length=80)
    user_name = models.CharField(max_length=80)
    user_token = models.CharField(max_length=80)
