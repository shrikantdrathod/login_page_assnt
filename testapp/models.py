from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.


class UserRegister(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phoneNo = models.BigIntegerField(unique=True)
    userName = models.CharField(max_length=100)
    password = models.CharField(max_length=10, validators=[MinLengthValidator(8)])
    rpassword = models.CharField(max_length=10)

    class Meta:
        db_table = 'userinfo'