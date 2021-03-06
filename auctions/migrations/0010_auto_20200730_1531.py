# Generated by Django 3.0.8 on 2020-07-30 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_listing_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='auctions.Category'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='upload',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
