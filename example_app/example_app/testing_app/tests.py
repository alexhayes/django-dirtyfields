from django.core.management.color import no_style
from django.db import models
from django.test import TestCase
from django.conf import settings
from django.core.management import call_command
from django.db.models.loading import load_app
from django.db import connection, transaction
from datetime import datetime

from example_app.testing_app.models import TestModel, ForeignTestModel, ManyToManyTestModel
from dirtyfields.helpers import get_changes

class DirtyFieldsMixinTestCase(TestCase):

    def test_dirty_fields(self):
        tm = TestModel()
        # initial state shouldn't be dirty
        self.assertEqual(tm.get_dirty_fields(), {})

        # changing values should flag them as dirty
        tm.boolean = False
        tm.characters = 'testing'
        self.assertEqual(tm.get_dirty_fields(), {
            'boolean': True,
            'characters': ''
        })

        # resetting them to original values should unflag
        tm.boolean = True
        self.assertEqual(tm.get_dirty_fields(), {
            'characters': ''
        })

    def test_sweeping(self):
        tm = TestModel()
        tm.boolean = False
        tm.characters = 'testing'
        self.assertEqual(tm.get_dirty_fields(), {
            'boolean': True,
            'characters': ''
        })
        tm.save()
        self.assertEqual(tm.get_dirty_fields(), {})


    def test_foreign_key(self):
        tm = TestModel()
        tm.save()
        self.assertEqual(tm.get_dirty_fields(), {})

        foreign_model = ForeignTestModel(name="Foreign")
        foreign_model.save()
        tm.foreign = foreign_model
        self.assertEqual(tm.get_dirty_fields(), {
                'foreign_id': None})
        tm.save()
        self.assertEqual(tm.get_dirty_fields(), {})

    def test_many_to_many(self):
        tm = TestModel()
        tm.save()
        self.assertEqual(tm.get_dirty_fields(), {})

        m2m_model = ManyToManyTestModel(name="m2m")
        m2m_model.save()
        tm.many_to_many.add(m2m_model)
        self.assertEqual(tm.get_dirty_fields(), {
                'many_to_many': set() })
        tm.save()
        self.assertEqual(tm.get_dirty_fields(), {})

        second_m2m_model = ManyToManyTestModel(name="m2m_second")
        second_m2m_model.save()
        tm.many_to_many.add(second_m2m_model)
        self.assertEqual(tm.get_dirty_fields(), {
                'many_to_many': set([m2m_model.pk]) })
        tm.save()

    def test_datetime_change(self):
        tm = TestModel()
        # initial state shouldn't be dirty
        self.assertEqual(tm.get_dirty_fields(), {})

        # changing values should flag them as dirty
        dt = datetime(2013, 1, 1)
        tm.created = dt
        self.assertEqual(tm.get_dirty_fields(), {
            'created': None
        })

        # resetting them to original values should unflag
        tm.created = None
        self.assertEqual(tm.get_dirty_fields(), {})


class DirtyFieldsHelperTestCase(TestCase):
    
    def test_dirty_fields(self):
        tm = TestModel()
        # initial state shouldn't be dirty
        self.assertEqual(tm.get_dirty_fields(), {})

        # changing values should flag them as dirty
        tm.boolean = False
        tm.characters = 'testing'
        self.assertEqual(tm.get_dirty_fields(), {
            'boolean': True,
            'characters': ''
        })
        
        changes = get_changes(tm)
        self.assertEqual(changes['boolean']['existing'], True)
        self.assertEqual(changes['boolean']['new'], False)
        self.assertEqual(changes['characters']['existing'], '')
        self.assertEqual(changes['characters']['new'], 'testing')