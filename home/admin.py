from django.contrib import admin
from .models import WeekMotto


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


admin.site.register(WeekMotto, AdminWeekMotto)
