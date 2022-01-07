from django.contrib import admin
from .models import WeekMotto, Song, Agenda


# Register your models here.
class AdminWeekMotto(admin.ModelAdmin):
    list_display = ['id',
                    'title',
                    'date',
                    'gospels',
                    'epistle',
                    'old_testament',
                    'lecture',
                    'motto_short',
                    'motto_long',
                    'motto_api',
                    'update_date',
                    'creation_date',
                    ]


class AdminSong(admin.ModelAdmin):
    list_display = ['id',
                    'title',
                    'update_date',
                    'creation_date',
                    ]


class AdminAgenda(admin.ModelAdmin):
    list_display = ['id',
                    'church_tools_id',
                    'title',
                    'date',
                    'agenda_state',
                    'update_date',
                    'creation_date',
                    ]


admin.site.register(WeekMotto, AdminWeekMotto)
admin.site.register(Song, AdminSong)
admin.site.register(Agenda, AdminAgenda)
