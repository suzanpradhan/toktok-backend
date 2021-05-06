# Generated by Django 3.2 on 2021-04-28 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodsubtype',
            name='food',
        ),
        migrations.AddField(
            model_name='food',
            name='subtypes',
            field=models.ManyToManyField(to='restaurant.FoodSubType'),
        ),
    ]