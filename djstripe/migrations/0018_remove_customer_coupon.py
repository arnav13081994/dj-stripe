# Generated by Django 3.2.13 on 2022-07-11 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("djstripe", "0017_add_invoiceitem_discounts"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customer",
            name="coupon",
        ),
        migrations.RemoveField(
            model_name="customer",
            name="coupon_end",
        ),
        migrations.RemoveField(
            model_name="customer",
            name="coupon_start",
        ),
    ]