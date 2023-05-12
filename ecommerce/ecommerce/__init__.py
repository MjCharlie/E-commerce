from django.db import models

# Create your models here.
class login(models.Model):
    logid = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField()
    number = models.IntegerField()
    dob = models.DateField()
    def __str__(self) -> str:
        return f"{name}+{logid}"
