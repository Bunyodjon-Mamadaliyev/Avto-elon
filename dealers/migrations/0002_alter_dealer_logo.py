# Generated by Django 5.2 on 2025-04-22 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealer',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='logos/'),
        ),
    ]
