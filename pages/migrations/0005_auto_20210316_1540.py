# Generated by Django 3.1.7 on 2021-03-16 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20210316_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='topic',
            field=models.CharField(max_length=20),
        ),
    ]
