# Generated by Django 5.1.1 on 2025-01-04 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_company_username_employee_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyemployee',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], max_length=50, null=True),
        ),
    ]
