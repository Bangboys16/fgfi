# Generated by Django 5.1.1 on 2024-10-16 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church', '0007_alter_branch_latitude_alter_branch_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]