# Generated by Django 5.1.3 on 2024-12-05 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0009_allowance_deduction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='allowance',
            old_name='amount',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='deduction',
            old_name='amount',
            new_name='value',
        ),
        migrations.RemoveField(
            model_name='allowance',
            name='percentage',
        ),
        migrations.RemoveField(
            model_name='deduction',
            name='percentage',
        ),
        migrations.AddField(
            model_name='allowance',
            name='calculation_type',
            field=models.CharField(choices=[('fixed', 'Fixed Amount'), ('percentage', 'Percentage of Base Salary')], default='fixed', max_length=10),
        ),
        migrations.AddField(
            model_name='deduction',
            name='calculation_type',
            field=models.CharField(choices=[('fixed', 'Fixed Amount'), ('percentage', 'Percentage of Base Salary')], default='fixed', max_length=10),
        ),
    ]
