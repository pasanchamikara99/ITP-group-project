from django.forms import ModelForm
from django.db import models



class EmployeesReg(models.Model):
    empid = models.CharField(max_length=45)
    fname = models.CharField(max_length=45)
    lname = models.CharField(max_length=45)
    email = models.EmailField()
    position = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    class Meta:
        db_table = "Employee"