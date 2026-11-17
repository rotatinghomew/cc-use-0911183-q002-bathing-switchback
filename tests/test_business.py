import unittest
from rotation.app import Application
from rotation.store import Store
from rotation.allocation import assignment_at, attendance, save_assignment
from rotation.services import descriptive_periods, save_service
from rotation.planning import course_costs, quote_expansion


class RotationTests(unittest.TestCase):
    def setUp(self):
        self.store = Store(':memory:')
        Application(self.store).seed()

    def tearDown(self):
        self.store.close()

    def test_boundary_allocation(self):
        self.assertEqual(assignment_at(self.store, 'east', '2026-10-08')['arm'], 'trained')

    def test_outside_period(self):
        self.assertIsNone(assignment_at(self.store, 'east', '2026-11-01'))

    def test_attendance_is_not_assignment(self):
        self.assertEqual(attendance(self.store, 'c1'), ['p3'])

    def test_missing_score_not_zero(self):
        periods = {row['assignment']: row for row in descriptive_periods(self.store)['periods']}
        self.assertIsNone(periods['a2']['score_mean'])
        self.assertEqual(periods['a2']['completed'], 0)

    def test_overlap_fails(self):
        row = dict(self.store.get('assignments', 'a1'), id='other')
        with self.assertRaises(ValueError):
            save_assignment(self.store, row)

    def test_bad_score_fails(self):
        row = dict(self.store.get('services', 's1'), score=8)
        with self.assertRaises(ValueError):
            save_service(self.store, row)

    def test_unknown_services_reported(self):
        row = dict(self.store.get('services', 's1'), id='later', date='2027-01-01')
        save_service(self.store, row)
        self.assertEqual(descriptive_periods(self.store)['unassigned'], ['later'])

    def test_course_cost_uses_registered_hours(self):
        self.assertEqual(course_costs(self.store)[0]['cents'], 32000)

    def test_expansion_budget(self):
        self.assertEqual(quote_expansion(self.store, ['north', 'south'])['service_slots'], 75)

    def test_duplicate_candidate_rejected(self):
        with self.assertRaises(ValueError):
            quote_expansion(self.store, ['north', 'north'])
