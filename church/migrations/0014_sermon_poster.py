# Generated by Django 5.1.1 on 2024-11-03 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church', '0013_sermon_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='sermon',
            name='poster',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
