# Generated by Django 4.2.6 on 2023-11-23 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_category_c_buy_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='c_buy_count',
        ),
    ]