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



class Leave(models.Model):
    date = models.CharField(max_length=45)
    empid = models.CharField(max_length=45)
    reason = models.CharField(max_length=255)
    status = models.CharField(max_length=45)
    leaveType = models.CharField(max_length=45)
    class Meta:
        db_table = "leave"


class employee_positions(models.Model):

    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
   
    class Meta:
        db_table = "emp_positions"


class leave_types(models.Model):

    leave_type = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
   
    class Meta:
        db_table = "leave_types"