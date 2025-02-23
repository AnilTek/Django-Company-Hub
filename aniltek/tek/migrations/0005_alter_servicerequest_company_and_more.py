# Generated by Django 5.1.1 on 2025-01-16 16:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tek', '0004_alter_servicerequest_calisma_ruhsati_and_more'),
        ('users', '0004_companyemployee_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicerequest',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_history', to='users.company'),
        ),
        migrations.AlterField(
            model_name='servicerequest',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_history', to='users.employee'),
        ),
        migrations.AlterField(
            model_name='servicerequest',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='request_history', to='tek.service'),
        ),
        migrations.AlterField(
            model_name='servicerequest',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='ServiceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('created', 'Created')], max_length=50, null=True)),
                ('date_submitted', models.DateField(blank=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_requests', to='users.company')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_requests', to='users.employee')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='tek.service')),
            ],
        ),
    ]
