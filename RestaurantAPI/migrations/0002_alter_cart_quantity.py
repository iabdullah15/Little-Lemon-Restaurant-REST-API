# Generated by Django 4.1.5 on 2023-01-16 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestaurantAPI', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.SmallIntegerField(default=1),
        ),
    ]