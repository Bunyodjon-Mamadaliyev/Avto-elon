# Generated by Django 5.2 on 2025-04-24 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_listing_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='primary_image',
            field=models.ImageField(default='default_listing.jpg', upload_to='images/'),
        ),
    ]
