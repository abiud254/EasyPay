# Generated by Django 5.1.3 on 2024-12-16 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0022_alter_employee_branch_alter_employee_department_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allowance',
            name='calculation_type',
        ),
        migrations.RemoveField(
            model_name='allowance',
            name='default_value',
        ),
    ]