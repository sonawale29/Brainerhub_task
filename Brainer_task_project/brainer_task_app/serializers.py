# In serializers.py
from rest_framework import serializers
from .models import Employee, Company

class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['employee_id', 'first_name', 'last_name', 'phone_number', 'salary', 'manager_id', 'department_id', 'company_name']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_name']
