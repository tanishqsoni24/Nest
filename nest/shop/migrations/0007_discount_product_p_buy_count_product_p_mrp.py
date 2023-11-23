# Generated by Django 4.2.6 on 2023-11-23 10:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_remove_category_c_buy_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('d_percentage', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='product',
            name='p_buy_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='p_mrp',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
