# Generated by Django 4.2.7 on 2023-11-24 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board_app', '0002_alter_subscription_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='posts',
            old_name='categories',
            new_name='category',
        ),
    ]
