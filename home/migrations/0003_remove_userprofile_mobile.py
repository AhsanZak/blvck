# Generated by Django 3.1.3 on 2020-11-26 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_userprofile_mobile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='mobile',
        ),
    ]
