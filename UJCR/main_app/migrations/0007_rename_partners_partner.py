# Generated by Django 4.0.2 on 2022-03-26 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_partners'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Partners',
            new_name='Partner',
        ),
    ]