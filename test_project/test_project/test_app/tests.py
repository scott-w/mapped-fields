from datetime import date, datetime
from decimal import Decimal
from unittest import TestCase

import mapped_fields

from test_project.test_app import forms


class MappedFieldTestCase(TestCase):
    """Tests to make sure the field mappings all work cleanly.
    """
    def test_widget_inheritance(self):
        """The correct Widget subclasses are used.
        """
        form = forms.TestForm()

        self.assertTrue(isinstance(
            form.fields['first_name'].widget,
            mapped_fields.widgets.MappedTextInput))

        self.assertTrue(isinstance(
            form.fields['last_name'].widget,
            mapped_fields.widgets.MappedTextInput))

        self.assertTrue(isinstance(
            form.fields['date_of_birth'].widget,
            mapped_fields.widgets.MappedDateInput))

        self.assertTrue(isinstance(
            form.fields['last_contacted'].widget,
            mapped_fields.widgets.MappedDateTimeInput))

        self.assertTrue(isinstance(
            form.fields['height'].widget,
            mapped_fields.widgets.MappedNumberInput))

        self.assertTrue(isinstance(
            form.fields['number_of_tshirts'].widget,
            mapped_fields.widgets.MappedNumberInput))

    def test_valid_contact(self):
        """We can set all the valid fields.
        """
        contact = {
            'FirstName': 'First',
            'Last Name': 'Last',
            'DateOfBirth': '1990-1-11',
            'last_call': '2014-03-21 15:16:17',
            'height_m': '1.73',
            'Tshirts': '15',
        }

        form = forms.TestForm(data=contact)

        self.assertTrue(form.is_valid())

        self.assertEqual(form.cleaned_data['first_name'], 'First')
        self.assertEqual(form.cleaned_data['last_name'], 'Last')
        self.assertEqual(
            form.cleaned_data['date_of_birth'], date(1990, 1, 11))
        # Tricky to deal with offset-aware datetime cleanly
        self.assertTrue(
            isinstance(form.cleaned_data['last_contacted'], datetime))
        self.assertEqual(form.cleaned_data['height'], Decimal('1.73'))
        self.assertEqual(form.cleaned_data['number_of_tshirts'], 15)

    def test_invalid_field(self):
        """The mapped fields work the same way as normal Django Fields.
        """
        contact = {
            'FirstName': 'First',
            'Last Name': 'Last',
            'DateOfBirth': 'Not Valid',
            'Tshirts': '15',
        }

        form = forms.TestForm(data=contact)

        self.assertFalse(form.is_valid())

        self.assertTrue('date_of_birth' in form.errors)
        self.assertTrue('last_contacted' in form.errors)
        self.assertTrue('height' in form.errors)


class MappedBooleanFieldTestCase(TestCase):
    """Tests specific to BooleanFields
    """
    def test_widget_inheritance(self):
        """The correct Widget subclasses are used.
        """
        form = forms.BooleanTestForm()

        self.assertTrue(isinstance(
            form.fields['is_staff'].widget,
            mapped_fields.widgets.MappedCheckboxInput))

        self.assertTrue(isinstance(
            form.fields['has_file'].widget,
            mapped_fields.widgets.MappedCheckboxInput))

    def test_true(self):
        """BooleanFields work as expected for 'truthy' values.
        """
        contact = {
            'staff_member': 'yes',
            'documented': 'true',
        }

        form = forms.BooleanTestForm(data=contact)

        self.assertTrue(form.is_valid())

        self.assertEqual(form.cleaned_data['is_staff'], True)
        self.assertEqual(form.cleaned_data['has_file'], True)

    def test_false(self):
        """BooleanFields work as expected for 'falsey' values.
        """
        contact = {
            'staff_member': 'false',
            'documented': '',
        }

        form = forms.BooleanTestForm(data=contact)

        self.assertFalse(form.is_valid())

        self.assertTrue('is_staff' in form.errors)
        self.assertEqual(form.cleaned_data['has_file'], False)
