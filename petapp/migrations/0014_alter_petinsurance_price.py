# Generated by Django 5.0.1 on 2024-12-08 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0013_alter_petinsurance_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petinsurance',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
