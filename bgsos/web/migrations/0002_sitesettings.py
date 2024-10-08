# Generated by Django 5.0.6 on 2024-09-06 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website_title', models.CharField(blank=True, max_length=100, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos/')),
                ('banner', models.ImageField(blank=True, null=True, upload_to='banners/')),
                ('banner_headline', models.CharField(blank=True, max_length=255, null=True)),
                ('banner_subheading', models.CharField(blank=True, max_length=255, null=True)),
                ('banner_button_text', models.CharField(blank=True, max_length=50, null=True)),
                ('banner_button_url', models.URLField(blank=True, null=True)),
                ('xmr_fixed_address', models.CharField(blank=True, max_length=100, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Site Setting',
                'verbose_name_plural': 'Site Settings',
            },
        ),
    ]
