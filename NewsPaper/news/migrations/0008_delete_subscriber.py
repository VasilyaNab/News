# Generated by Django 5.1.5 on 2025-02-06 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_alter_subscriber_unique_together_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Subscriber',
        ),
    ]
