# Generated by Django 4.2.13 on 2024-07-25 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_friendship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.CharField(default='default.svg', max_length=255),
        ),
    ]
