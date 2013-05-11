from django.forms.models import model_to_dict
from django.db import models

class JournalEntry(models.Model):
    shared_date = models.DateTimeField('date published')
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title

    def to_dict(self):
        e = model_to_dict(self)
        e['shared_date'] = str(self.shared_date)
        return e
