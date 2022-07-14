# Generated by Django 3.2.13 on 2022-07-13 07:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import djstripe.enums
import djstripe.fields


class Migration(migrations.Migration):

    dependencies = [
        ("djstripe", "0011_2_7"),
    ]

    operations = [
        migrations.CreateModel(
            name="LineItem",
            fields=[
                ("djstripe_created", models.DateTimeField(auto_now_add=True)),
                ("djstripe_updated", models.DateTimeField(auto_now=True)),
                ("djstripe_id", models.BigAutoField(primary_key=True, serialize=False)),
                ("id", djstripe.fields.StripeIdField(max_length=255, unique=True)),
                ("livemode", models.BooleanField(blank=True, default=None, null=True)),
                ("created", djstripe.fields.StripeDateTimeField(blank=True, null=True)),
                ("metadata", djstripe.fields.JSONField(blank=True, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("amount", djstripe.fields.StripeQuantumCurrencyAmountField()),
                (
                    "amount_excluding_tax",
                    djstripe.fields.StripeQuantumCurrencyAmountField(),
                ),
                ("currency", djstripe.fields.StripeCurrencyCodeField(max_length=3)),
                ("discount_amounts", djstripe.fields.JSONField(blank=True, null=True)),
                ("discountable", models.BooleanField(default=False)),
                ("discounts", djstripe.fields.JSONField(blank=True, null=True)),
                ("period", djstripe.fields.JSONField()),
                ("period_end", djstripe.fields.StripeDateTimeField()),
                ("period_start", djstripe.fields.StripeDateTimeField()),
                ("price", djstripe.fields.JSONField()),
                ("proration", models.BooleanField(default=False)),
                ("proration_details", djstripe.fields.JSONField()),
                ("tax_amounts", djstripe.fields.JSONField(blank=True, null=True)),
                ("tax_rates", djstripe.fields.JSONField(blank=True, null=True)),
                (
                    "type",
                    djstripe.fields.StripeEnumField(
                        enum=djstripe.enums.LineItem, max_length=12
                    ),
                ),
                (
                    "unit_amount_excluding_tax",
                    djstripe.fields.StripeDecimalCurrencyAmountField(
                        blank=True, decimal_places=2, max_digits=11, null=True
                    ),
                ),
                ("quantity", models.IntegerField(blank=True, null=True)),
                (
                    "djstripe_owner_account",
                    djstripe.fields.StripeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="djstripe.account",
                        to_field=settings.DJSTRIPE_FOREIGN_KEY_TO_FIELD,
                    ),
                ),
                (
                    "invoice_item",
                    djstripe.fields.StripeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="djstripe.invoiceitem",
                        to_field=settings.DJSTRIPE_FOREIGN_KEY_TO_FIELD,
                    ),
                ),
                (
                    "subscription",
                    djstripe.fields.StripeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="djstripe.subscription",
                        to_field=settings.DJSTRIPE_FOREIGN_KEY_TO_FIELD,
                    ),
                ),
                (
                    "subscription_item",
                    djstripe.fields.StripeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="djstripe.subscriptionitem",
                        to_field=settings.DJSTRIPE_FOREIGN_KEY_TO_FIELD,
                    ),
                ),
            ],
            options={
                "get_latest_by": "created",
                "abstract": False,
            },
        ),
    ]
