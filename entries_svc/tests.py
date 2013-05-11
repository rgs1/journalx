from django.test import TestCase
from django.utils import timezone

from models import JournalEntry
import json

class SimpleTest(TestCase):
    def test_json_representation(self):
        """
        Client libraries are expecting to consume this, so lets test
        """
        d = timezone.now()
        expected_serialized_entry = {
            'title': 'test1',
            'desc': 'desc1',
            'id': 1,
            'shared_date': str(d)
            }
        e = JournalEntry(title='test1',
                         desc='desc1',
                         shared_date=d)
        e.save()

        self.assertEqual(json.loads(json.dumps(expected_serialized_entry)),
                         e.to_dict())
