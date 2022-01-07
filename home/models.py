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


class Song(models.Model):
    id = models.AutoField(primary_key=True)
    filePath = models.CharField('Dateipfad', blank=False, null=False, unique=True, max_length=400)
    title = models.CharField('Titel', blank=False, null=False, max_length=100)

    copyrights = models.CharField('(c)', blank=True, null=True, max_length=500)
    addCopyrightInfo = models.CharField('AddCopyrightInfo', blank=True, null=True, max_length=500)
    author = models.CharField('Author', blank=True, null=True, max_length=200)
    bible = models.CharField('Bible', blank=True, null=True, max_length=100)
    CCLI = models.IntegerField('CCLI', blank=True, null=True)
    categories = models.CharField('Categories', blank=True, null=True, max_length=100)
    churchSongID = models.CharField('ChurchSongID', blank=True, null=True, max_length=100)
    comment = models.CharField('Comment', blank=True, null=True, max_length=100)
    editor = models.CharField('Editor', blank=True, null=True, max_length=100)
    format = models.CharField('Format', blank=True, null=True, max_length=100)
    key = models.CharField('Key', blank=True, null=True, max_length=20)
    keywords = models.CharField('Keywords', blank=True, null=True, max_length=200)
    lang = models.CharField('Lang', blank=True, null=True, max_length=100)
    langCount = models.IntegerField('LangCount', blank=True, null=True)
    melody = models.CharField('Melody', blank=True, null=True, max_length=100)
    natCopyright = models.CharField('NatCopyright', blank=True, null=True, max_length=500)
    oTitle = models.CharField('OTitle', blank=True, null=True, max_length=100)
    quickFind = models.CharField('QuickFind', blank=True, null=True, max_length=50)
    rights = models.CharField('Rights', blank=True, null=True, max_length=500)
    songbook = models.CharField('Songbook', blank=True, null=True, max_length=100)
    speed = models.CharField('Speed', blank=True, null=True, max_length=20)
    titleFormat = models.CharField('TitleFormat', blank=True, null=True, max_length=20)
    titleLang2 = models.CharField('TitleLang2', blank=True, null=True, max_length=100)
    titleLang3 = models.CharField('TitleLang3', blank=True, null=True, max_length=100)
    titleLang4 = models.CharField('TitleLang4', blank=True, null=True, max_length=100)
    translation = models.CharField('Translation', blank=True, null=True, max_length=100)
    verseOrder = models.CharField('VerseOrder', blank=True, null=True, max_length=500)
    version = models.CharField('Version', blank=True, null=True, max_length=20)

    file_md5_hash = models.CharField('md5-Hash', blank=False, null=False, max_length=32)
    content = models.TextField('Inhalt', blank=False, null=False)

    update_date = models.DateTimeField('Geändert', auto_now=True)
    creation_date = models.DateTimeField('Erstellt', auto_now_add=True)

    class Meta:
        verbose_name_plural = "Songs"

    def __str__(self):
        return self.title


class Agenda(models.Model):
    id = models.AutoField(primary_key=True)
    church_tools_id = models.IntegerField('ChurchTools ID', unique=True, blank=False, null=False)
    title = models.CharField('Titel', blank=True, max_length=100)
    date = models.DateTimeField('Datum', blank=False)
    agenda_state = models.BooleanField('Agenda-Status')
    content = models.TextField('Inhalt', blank=False, null=False)

    update_date = models.DateTimeField('Geändert', auto_now=True)
    creation_date = models.DateTimeField('Erstellt', auto_now_add=True)

    class Meta:
        verbose_name_plural = "Agendas"

    def __str__(self):
        return self.title + str(self.date)
