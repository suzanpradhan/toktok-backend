# Generated by Django 3.2 on 2021-07-14 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storemanagerapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storemanagerbasicdetail',
            name='token',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
