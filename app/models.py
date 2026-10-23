from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    address=models.TextField()
    profile_pic=models.ImageField()
    username=models.OneToOneField(User,on_delete=models.CASCADE)

