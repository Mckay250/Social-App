# Generated by Django 3.2.9 on 2021-11-26 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ip_address',
            field=models.GenericIPAddressField(null=True),
        ),
    ]
