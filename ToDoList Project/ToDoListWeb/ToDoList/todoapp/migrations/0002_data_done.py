# Generated by Django 2.2.14 on 2020-07-30 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
