# Generated by Django 2.1.4 on 2019-08-31 04:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='lastName',
        ),
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
    ]
