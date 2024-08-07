# Generated by Django 4.2.13 on 2024-07-07 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_remove_notification_title_remove_notification_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('event_created', 'Event Created'), ('event_updated', 'Event Updated'), ('event_cancelled', 'Event Cancelled'), ('invitation_response', 'Invitation Response'), ('suggested_alternate_date', 'Suggested Alternate Date'), ('event_confirmed', 'Event Confirmed')], max_length=50),
        ),
    ]
