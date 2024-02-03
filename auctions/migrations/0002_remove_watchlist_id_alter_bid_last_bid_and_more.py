# Generated by Django 5.0.1 on 2024-01-30 07:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="watchlist",
            name="id",
        ),
        migrations.AlterField(
            model_name="bid",
            name="last_bid",
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name="watchlist",
            name="product_id",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                serialize=False,
                to="auctions.list_item",
            ),
        ),
    ]