# Generated by Django 4.1.1 on 2022-10-02 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stors', '0003_cart_ordered_cart_ordered_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='ordered_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
