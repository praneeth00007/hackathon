# Generated by Django 5.1.1 on 2024-12-07 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0005_userregistrationlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
    ]
