# Generated by Django 3.2.4 on 2021-07-10 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagegallery', '0002_alter_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.FileField(upload_to='images/'),
        ),
    ]
