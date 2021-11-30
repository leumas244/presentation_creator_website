from django.db import models


# Create your models here.
class WeekMotto(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField('Titel', blank=True, null=True, default='', max_length=100)
    date = models.DateField('Datum', blank=False)
    gospels = models.CharField('Evangelien', blank=True, null=True, default='', max_length=500)
    epistle = models.CharField('Epistel', blank=True, null=True, default='', max_length=500)
    old_testament = models.CharField('AT', blank=True, null=True, default='', max_length=500)
    lecture = models.CharField('Predigt', blank=True, null=True, default='', max_length=100)
    motto_short = models.CharField('Wochenspruch kurz', blank=False, null=True, default='', max_length=100)
    motto_long = models.CharField('Wochenspruch Lang', blank=True, null=True, default='', max_length=200)
    motto_api = models.CharField('Wochenspruch API', blank=True, null=True, default='', max_length=200)
    update_date = models.DateTimeField('Geändert', auto_now=True)
    creation_date = models.DateTimeField('Erstellt', auto_now_add=True)

    class Meta:
        verbose_name_plural = "WeekMottos"

    def __str__(self):
        return self.title
