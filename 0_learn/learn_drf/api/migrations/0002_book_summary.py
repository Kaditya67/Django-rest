# Generated by Django 5.1.4 on 2024-12-10 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='summary',
            field=models.TextField(blank=True, null=True),
        ),
    ]
