# Generated by Django 3.2 on 2021-07-14 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restaurant', '0001_initial'),
        ('storemanagerapp', '0001_initial'),
        ('basicapp', '0001_initial'),
        ('imagegallery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtype',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='storemanagerapp.storemanagerbasicdetail'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='cover_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='imagegallery.image'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicapp.location'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='storemanagerapp.storemanagerbasicdetail'),
        ),
        migrations.AddField(
            model_name='menucollection',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='storemanagerapp.storemanagerbasicdetail'),
        ),
        migrations.AddField(
            model_name='foodsubtype',
            name='subtype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.subtype'),
        ),
        migrations.AddField(
            model_name='foodcombo',
            name='addons',
            field=models.ManyToManyField(to='restaurant.Addons'),
        ),
        migrations.AddField(
            model_name='foodcombo',
            name='cover_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='imagegallery.image'),
        ),
        migrations.AddField(
            model_name='foodcombo',
            name='foods',
            field=models.ManyToManyField(to='restaurant.Food'),
        ),
        migrations.AddField(
            model_name='foodcombo',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='storemanagerapp.storemanagerbasicdetail'),
        ),
        migrations.AddField(
            model_name='food',
            name='MenuCollection',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.menucollection'),
        ),
        migrations.AddField(
            model_name='food',
            name='addons',
            field=models.ManyToManyField(to='restaurant.Addons'),
        ),
        migrations.AddField(
            model_name='food',
            name='cover_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='imagegallery.image'),
        ),
        migrations.AddField(
            model_name='food',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='storemanagerapp.storemanagerbasicdetail'),
        ),
        migrations.AddField(
            model_name='food',
            name='subtypes',
            field=models.ManyToManyField(to='restaurant.FoodSubType'),
        ),
        migrations.AddField(
            model_name='addons',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='storemanagerapp.storemanagerbasicdetail'),
        ),
    ]
