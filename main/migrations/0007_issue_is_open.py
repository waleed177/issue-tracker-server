# Generated by Django 3.2.4 on 2021-08-07 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210807_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='is_open',
            field=models.BooleanField(default=True),
        ),
    ]