# Generated by Django 3.2.5 on 2021-08-08 10:45

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_extenduser_declined_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='extenduser',
            name='cover_image',
            field=models.ImageField(default='default_cover.jpeg', upload_to=users.models.upload_path_cover),
        ),
    ]
