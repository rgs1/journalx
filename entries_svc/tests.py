from django.test import TestCase

from models import JournalEntry
import json

class SimpleTest(TestCase):
    def test_json_representation(self):
        """
        Client libraries are expecting to consume this, so lets test
        """
        expected_serialized_entry = {
            'title': 'test1',
            'desc': 'desc1',
            }
        expected_reloaded = json.loads(json.dumps(expected_serialized_entry))

        e = JournalEntry(title='test1',
                         desc='desc1')
        e.save()
        e_as_dict = e.to_dict()

        self.assertEqual(expected_reloaded['title'], e_as_dict['title'])
        self.assertEqual(expected_reloaded['desc'], e_as_dict['desc'])

