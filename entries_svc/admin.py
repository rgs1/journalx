from entries_svc.models import JournalEntry
from django.contrib import admin

class JournalEntryAdmin(admin.ModelAdmin):
    fields = ['title', 'desc', 'screenshot']
    list_display = ('title', 'desc', 'shared_date')
admin.site.register(JournalEntry, JournalEntryAdmin)
