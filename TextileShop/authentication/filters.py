import django_filters
from .models import EmployeesReg


class listPositionsfilter(django_filters.FilterSet):

    class Meta:
        model = EmployeesReg
        fields  = {'position' : ['exact']}
