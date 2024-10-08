# Generated by Django 5.0.6 on 2024-09-10 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_sitesettings_contact_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='display_social_links',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='facebook',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='instagram',
            field=models.URLField(blank=True, null=True),
        ),
    ]
