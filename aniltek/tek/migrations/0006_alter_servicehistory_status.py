# Generated by Django 5.1.1 on 2025-01-16 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tek', '0005_alter_servicerequest_company_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicehistory',
            name='status',
            field=models.CharField(blank=True, choices=[('created', 'Created')], default='Created', max_length=50, null=True),
        ),
    ]
