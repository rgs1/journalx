from django.forms.models import model_to_dict
from django.db import models
from django.utils import timezone

class JournalUser(models.Model):
    sugar_id = models.CharField(max_length=200)

    def __unicode__(self):
        return self.sugar_id

class JournalEntry(models.Model):
    owner = models.ForeignKey(JournalUser)
    shared_date = models.DateTimeField('date published')
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    screenshot = models.ImageField(upload_to='screenshots')

    def save(self, *args, **kwargs):
        self.shared_date = timezone.now()
        super(JournalEntry, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def to_dict(self):
        e = model_to_dict(self)
        e.pop('screenshot')
        e['shared_date'] = str(self.shared_date)
        return e

class Comment(models.Model):
    entry = models.ForeignKey(JournalEntry)
    text = models.CharField(max_length=200)

    def __unicode__(self):
        return self.text

    def to_dict(self):
        e = model_to_dict(self)
        e['entry_id'] = e['entry']
        e.pop('entry')
        return e
