# Generated by Django 3.1.3 on 2020-11-21 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20201121_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateField(auto_now_add=True),
        ),
    ]
