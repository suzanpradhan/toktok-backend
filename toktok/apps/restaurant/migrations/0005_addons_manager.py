# Generated by Django 3.2 on 2021-05-06 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storemanagerapp', '0001_initial'),
        ('restaurant', '0004_alter_food_menucollection'),
    ]

    operations = [
        migrations.AddField(
            model_name='addons',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='storemanagerapp.storemanagerbasicdetail'),
        ),
    ]