# Generated by Django 4.2.13 on 2024-07-05 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_alter_event_status'),
        ('invitations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='events.event'),
        ),
    ]
