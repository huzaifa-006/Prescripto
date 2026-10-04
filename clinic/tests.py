from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import MedicineForm, PrescriptionMedicineForm
from .models import Patient, Prescription, PrescriptionMedicine


class PrescriptionPrintViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testdoctor", password="testpass123")
        self.client.force_login(self.user)
        self.patient = Patient.objects.create(name="Test Patient", gender="M", age=30)
        self.prescription = Prescription.objects.create(patient=self.patient)

    def test_prescription_print_page_renders(self):
        response = self.client.get(
            reverse("prescription_print", kwargs={"pk": self.prescription.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clinic/prescription_print.html")

    def test_prescription_print_shows_medicine_instructions(self):
        PrescriptionMedicine.objects.create(
            prescription=self.prescription,
            custom_medicine="Test Medicine",
            instructions="After food",
        )

        response = self.client.get(
            reverse("prescription_print", kwargs={"pk": self.prescription.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Instructions")
        self.assertContains(response, "کھانے کے بعد")

    def test_prescription_print_and_detail_shows_dosage_timing(self):
        from decimal import Decimal
        PrescriptionMedicine.objects.create(
            prescription=self.prescription,
            custom_medicine="Augmentin",
            morning=Decimal('0.5'),
            afternoon=Decimal('1'),
            evening=Decimal('0'),
            night=Decimal('1.5'),
        )

        # Test Print View
        response = self.client.get(
            reverse("prescription_print", kwargs={"pk": self.prescription.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "0.5")
        self.assertContains(response, "1.5")

        # Test Detail View
        detail_response = self.client.get(
            reverse("prescription_detail", kwargs={"pk": self.prescription.pk})
        )
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "0.5")
        self.assertContains(detail_response, "1.5")

    def test_prescription_print_shows_custom_vitals_only_when_filled(self):
        self.prescription.blood_pressure = "120/80"
        self.prescription.sugar = "140 mg/dL"
        self.prescription.other_vitals = "SpO2 on exertion: 92%"
        self.prescription.save()

        response = self.client.get(
            reverse("prescription_print", kwargs={"pk": self.prescription.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BP:")
        self.assertContains(response, "120/80")
        self.assertContains(response, "Sugar:")
        self.assertContains(response, "140 mg/dL")
        self.assertContains(response, "Other:")
        self.assertContains(response, "SpO2 on exertion: 92%")

    def test_prescription_print_hides_empty_custom_vitals(self):
        response = self.client.get(
            reverse("prescription_print", kwargs={"pk": self.prescription.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "BP:")
        self.assertNotContains(response, "Sugar:")
        self.assertNotContains(response, "Other:")

    def test_prescription_print_shows_patient_id(self):
        response = self.client.get(
            reverse("prescription_print", kwargs={"pk": self.prescription.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.patient.patient_id)
        self.assertContains(response, "patient-id-corner")
        self.assertNotContains(response, "Patient ID:")

    def test_prescription_print_shows_vaccine_line_when_checked(self):
        self.prescription.influvac_vaccine = True
        self.prescription.save()

        response = self.client.get(
            reverse("prescription_print", kwargs={"pk": self.prescription.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2026/2027 Influvac /vaxigrip ...I/M once only")

    def test_prescription_print_hides_vaccine_line_when_not_checked(self):
        self.prescription.influvac_vaccine = False
        self.prescription.save()

        response = self.client.get(
            reverse("prescription_print", kwargs={"pk": self.prescription.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "2026/2027 Influvac /vaxigrip ...I/M once only")


class MedicineFormChoicesTests(TestCase):
    def test_medicine_form_includes_new_form_choices(self):
        form = MedicineForm()
        labels = [label for _, label in form.fields["form"].choices]

        self.assertIn("Nasal Spray", labels)
        self.assertIn("Nebulizer Solution", labels)
        self.assertIn("Dispersible Tablet", labels)
        self.assertIn("Gel", labels)
        self.assertIn("Ointment", labels)


class PrescriptionMedicineFormTests(TestCase):
    def test_instruction_dropdown_has_expected_choices(self):
        form = PrescriptionMedicineForm()
        labels = [label for _value, label in form.fields["instruction_choice"].choices]

        self.assertIn("کھانے سے پہلے (Before meal)", labels)
        self.assertIn("کھانے کے بعد (After meal)", labels)
        self.assertIn("سونے سے پہلے (Before sleep)", labels)
        self.assertIn("Custom Instruction", labels)

    def test_custom_instruction_is_saved_to_instructions_field(self):
        form = PrescriptionMedicineForm(
            data={
                "instruction_choice": "custom",
                "custom_instruction": "رات کو سونے سے پہلے",
                "instructions": "",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["instructions"], "رات کو سونے سے پہلے")

    def test_timing_dropdowns_have_expected_choices(self):
        form = PrescriptionMedicineForm()
        expected_values = ['0', '0.5', '1', '1.5', '2', '2.5', '3']
        for field_name in ['morning', 'afternoon', 'evening', 'night']:
            field = form.fields[field_name]
            values = [val for val, _ in field.choices]
            self.assertEqual(values, expected_values)
            self.assertEqual(field.widget.attrs.get('class'), 'form-control timing-select')

    def test_timing_dropdown_values_cleaned_and_saved_correctly(self):
        form = PrescriptionMedicineForm(
            data={
                "custom_medicine": "Paracetamol",
                "morning": "0.5",
                "afternoon": "1",
                "evening": "1.5",
                "night": "2.5",
                "days": "5",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["morning"], 0.5)
        self.assertEqual(form.cleaned_data["afternoon"], 1)
        self.assertEqual(form.cleaned_data["evening"], 1.5)
        self.assertEqual(form.cleaned_data["night"], 2.5)

    def test_prescription_medicine_display_properties(self):
        from decimal import Decimal
        patient = Patient.objects.create(name="Dosage Test Patient", gender="M", age=25)
        prescription = Prescription.objects.create(patient=patient)
        med = PrescriptionMedicine.objects.create(
            prescription=prescription,
            custom_medicine="Amoxicillin",
            morning=Decimal('0.5'),
            afternoon=Decimal('1.0'),
            evening=Decimal('0.0'),
            night=Decimal('2.5'),
        )
        self.assertEqual(med.morning_display, "0.5")
        self.assertEqual(med.afternoon_display, "1")
        self.assertEqual(med.evening_display, "")
        self.assertEqual(med.night_display, "2.5")
