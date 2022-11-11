# Generated by Django 4.0.5 on 2022-11-11 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_renderdpowerpointfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionaluserinfo',
            name='has_loged_in',
            field=models.BooleanField(default=False, verbose_name='War eingeloggt?'),
        ),
        migrations.AddField(
            model_name='additionaluserinfo',
            name='one_time_token',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Einmal-Token'),
        ),
        migrations.AddField(
            model_name='additionaluserinfo',
            name='token_expiry_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Token Ablauf Datum'),
        ),
    ]
