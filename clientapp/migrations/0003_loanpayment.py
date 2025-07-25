# Generated by Django 5.1.6 on 2025-07-01 01:11

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientapp', '0002_alter_staff_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('approval_status', models.TextField(choices=[('Approved', 'Approved'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Pending')),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientapp.loan')),
            ],
        ),
    ]
