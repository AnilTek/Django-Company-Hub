from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Company Model
class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)  # Hashlenecek
    date_joined = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.username or "Unnamed Company"


# Employee Model
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    surname = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)  # Hashlenecek
    date_joined = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.username or 'Unnamed'}"


# Many-to-Many Relationship Between Company and Employee
class CompanyEmployee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees', null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='companies', null=True, blank=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ],blank=True,null=True)
    date_joined = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)


    def __str__(self):
        return f"{self.employee.username or 'Unnamed'} at {self.company.username or 'Unnamed Company'}"


# Creating an Employee or Company instance based on user first_name which we use as an account type option
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        user_type = user.first_name 
        if user_type == 'Company':
            Company.objects.create(
                user=user,
                email=user.email,
                username=user.username,
                name=user.first_name
            )
        elif user_type == 'Employee':
            Employee.objects.create(
                user=user,
                email=user.email,
                username=user.username,
                name=user.first_name,
                surname=user.last_name,
                password=user.password
            )

post_save.connect(create_user_profile, sender=User)
