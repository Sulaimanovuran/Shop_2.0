# Generated by Django 4.0.6 on 2022-08-02 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='info',
            field=models.TextField(blank=True),
        ),
    ]
