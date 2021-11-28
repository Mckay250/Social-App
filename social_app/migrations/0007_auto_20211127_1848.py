# Generated by Django 3.2.9 on 2021-11-27 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0006_geolocationdata_userholidaydata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geolocationdata',
            name='country_code',
            field=models.CharField(default='', max_length=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='geolocationdata',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='geolocationdata',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
    ]