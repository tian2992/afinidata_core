# Generated by Django 2.2.10 on 2020-03-11 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instances', '0009_instanceassociationuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instance',
            name='user_id',
        ),
    ]
