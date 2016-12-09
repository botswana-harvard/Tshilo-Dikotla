from datetime import date
from django.test import TestCase

from edc_constants.constants import YES, NO

from ..forms import MaternalInterimIdccForm

from .test_mixins import AntenatalVisitsMotherMixin, PosMotherMixin


class TestMaternalInterimIdccDataForm(AntenatalVisitsMotherMixin, PosMotherMixin, TestCase):

    def setUp(self):
        super(TestMaternalInterimIdccDataForm, self).setUp()

        self.add_maternal_visits('1000M', '1010M')
        maternal_visit = self.get_maternal_visit('1010M')

        self.options = {
            'maternal_visit': maternal_visit.id,
            'info_since_lastvisit': YES,
            'recent_cd4': 2.80,
            'recent_cd4_date': date.today(),
            'value_vl_size': 'equal',
            'value_vl': 400,
            'recent_vl_date': date.today(),
            'other_diagnoses': 'Hepatitis B'}

    def test_recent_cd4_available_date_not_provided(self):
        """if there is a recent cd4 information available, the date it was obtained should be indicated"""
        self.options.update(recent_cd4_date=None)
        forms = MaternalInterimIdccForm(data=self.options)
        self.assertIn("You specified that there is recent cd4 information available,"
                      " please provide the date", forms.errors.get('__all__'))

    def test_recent_cd4_not_provided_date_provided(self):
        """test that the date of the recent cd4 is not provided without providing the cd4 value"""
        self.options.update(recent_cd4=None)
        forms = MaternalInterimIdccForm(data=self.options)
        self.assertIn("You provided the date for the CD4 information but have not"
                      " indicated the CD4 value", forms.errors.get('__all__'))

    def test_value_vl_size_less_than(self):
        """if the most recent VL is less_than a number, the value of the VL should be 400"""
        self.options.update(
            value_vl_size='less_than',
            value_vl=300)
        forms = MaternalInterimIdccForm(data=self.options)
        self.assertIn("You indicated that the value of the most recent VL is less_than a number,"
                      " therefore the value of VL should be 400", forms.errors.get('__all__'))

    def test_value_vl_size_greater_than(self):
        """if the most recent VL is greater_than a number, the value of the VL should be 750000"""
        self.options.update(
            value_vl_size='greater_than',
            value_vl=300)
        forms = MaternalInterimIdccForm(data=self.options)
        self.assertIn("You indicated that the value of the most recent VL is greater_than a number,"
                      " therefore the value of VL should be 750000", forms.errors.get('__all__'))

    def test_value_vl_size_equal_to(self):
        """if the most recent VL is equal to a number, the value of the VL should be between 400 and
           750000 inclusive"""
        self.options.update(value_vl=300)
        forms = MaternalInterimIdccForm(data=self.options)
        self.assertIn("You indicated that the value of the most recent VL is equal to a number,"
                      " therefore the value of VL should be between 400 and 750000"
                      "(inclusive of 400 and 750000)", forms.errors.get('__all__'))

    def test_recent_vl_value_date_not_provided(self):
        """If the VL value is provided then the date should be provided as well"""
        self.options.update(recent_vl_date=None)
        forms = MaternalInterimIdccForm(data=self.options)
        self.assertIn("You indicated that there was a VL value, please provide the"
                      " date it was determined", forms.errors.get('__all__'))

    def test_no_info_since_last_visit(self):
        """if there has not been any lab information since the last visit, questions on CD4, VL and diagnoses found
           should not be answered"""
        self.options.update(info_since_lastvisit=NO)
        forms = MaternalInterimIdccForm(data=self.options)
        self.assertIn("You indicated that there has not been any lab information since the last visit"
                      " please do not answer the questions on CD4, VL and diagnoses found", forms.errors.get('__all__'))
