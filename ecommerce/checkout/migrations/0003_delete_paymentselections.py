# Generated by Django 5.0.6 on 2024-05-24 03:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_alter_deliveryoptions_id_alter_paymentselections_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PaymentSelections',
        ),
    ]
