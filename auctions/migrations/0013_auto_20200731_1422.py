# Generated by Django 3.0.8 on 2020-07-31 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_bid_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Wishlist',
            new_name='Watchlist',
        ),
    ]
