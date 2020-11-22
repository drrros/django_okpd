from django.contrib import admin
from .models import Record

@admin.register(Record)
# admin.site.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'okpd',
        'ktru_records_count',
        'date_changed'
    )