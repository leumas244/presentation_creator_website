# Generated by Django 4.0 on 2022-01-03 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_song'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('church_tools_id', models.IntegerField(unique=True, verbose_name='ChurchTools ID')),
                ('title', models.CharField(blank=True, max_length=100, verbose_name='Titel')),
                ('date', models.DateTimeField(verbose_name='Datum')),
                ('agenda_state', models.BooleanField(verbose_name='Agenda-Status')),
                ('content', models.TextField(verbose_name='Inhalt')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Geändert')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Erstellt')),
            ],
            options={
                'verbose_name_plural': 'Agendas',
            },
        ),
    ]
