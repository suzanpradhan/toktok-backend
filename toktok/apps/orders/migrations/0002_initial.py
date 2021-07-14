# Generated by Django 3.2 on 2021-07-14 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restaurant', '0001_initial'),
        ('orders', '0001_initial'),
        ('storemanagerapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='storemanagerapp.storemanagerbasicdetail'),
        ),
        migrations.AddField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant'),
        ),
        migrations.AddField(
            model_name='foodorder',
            name='quantity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.food'),
        ),
    ]
