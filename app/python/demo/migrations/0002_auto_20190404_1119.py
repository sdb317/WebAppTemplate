# Generated by Django 2.1.8 on 2019-04-04 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='type',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='personaudit',
            name='type',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
