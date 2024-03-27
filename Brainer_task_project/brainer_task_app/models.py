from django.db import models

class Company(models.Model):
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name

class Employee(models.Model):
    employee_id = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    manager_id = models.CharField(max_length=20)
    department_id = models.CharField(max_length=20)
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees', null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"
