# Generated by Django 3.1.7 on 2021-03-18 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210310_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='extenduser',
            name='country',
            field=models.CharField(blank=True, max_length=255, verbose_name='country'),
        ),
    ]
