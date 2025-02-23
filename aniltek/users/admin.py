from django.contrib import admin

# Register your models here.

from .models import Company, Employee, CompanyEmployee

admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(CompanyEmployee)


# superuser : anil - anil