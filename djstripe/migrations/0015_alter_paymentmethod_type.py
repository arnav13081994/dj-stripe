# Generated by Django 3.2.9 on 2021-12-04 16:43

from django.db import migrations
import djstripe.enums
import djstripe.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djstripe', '0014_webhookeventtrigger_stripe_trigger_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethod',
            name='type',
            field=djstripe.fields.StripeEnumField(enum=djstripe.enums.PaymentMethodType, help_text='The type of the PaymentMethod.', max_length=17),
        ),
    ]
