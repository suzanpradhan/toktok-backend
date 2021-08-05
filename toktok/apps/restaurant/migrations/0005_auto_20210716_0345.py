# Generated by Django 3.2 on 2021-07-15 22:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imagegallery', '0001_initial'),
        ('restaurant', '0004_alter_food_subtypes'),
    ]

    operations = [
        migrations.AddField(
            model_name='menucollection',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='imagegallery.image'),
        ),
        migrations.AlterField(
            model_name='food',
            name='addons',
            field=models.ManyToManyField(blank=True, null=True, to='restaurant.Addons'),
        ),
    ]
