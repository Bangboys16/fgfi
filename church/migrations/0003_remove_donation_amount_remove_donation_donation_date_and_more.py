# Generated by Django 5.1.1 on 2024-10-08 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church', '0002_blogpost_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donation',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='donation',
            name='donation_date',
        ),
        migrations.RemoveField(
            model_name='donation',
            name='donor_name',
        ),
        migrations.RemoveField(
            model_name='donation',
            name='email',
        ),
        migrations.RemoveField(
            model_name='donation',
            name='message',
        ),
        migrations.RemoveField(
            model_name='service',
            name='date',
        ),
        migrations.AddField(
            model_name='donation',
            name='account_name',
            field=models.CharField(default='freegraceinternational', help_text="Enter the church's account name", max_length=100),
        ),
        migrations.AddField(
            model_name='donation',
            name='bank_name',
            field=models.CharField(default='Uba', help_text="Enter the church's bank name", max_length=100),
        ),
        migrations.AddField(
            model_name='service',
            name='day',
            field=models.CharField(default='Add day of service', max_length=20),
        ),
        migrations.AlterField(
            model_name='donation',
            name='bank_account',
            field=models.IntegerField(help_text="Enter the church's bank account details"),
        ),
    ]