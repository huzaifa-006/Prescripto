from django import forms
from .models import Patient, Medicine, Prescription, PrescriptionMedicine, LabTest


class PatientForm(forms.ModelForm):
    """Form for creating/editing patients"""
    class Meta:
        model = Patient
        fields = ['name', 'gender', 'age', 'weight', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patient Name'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight (kg)', 'step': '0.1'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Address'}),
        }


class MedicineForm(forms.ModelForm):
    """Form for adding/editing medicines"""
    class Meta:
        model = Medicine
        fields = ['name', 'form', 'strength', 'default_dosage', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Medicine Name'}),
            'form': forms.Select(attrs={'class': 'form-control'}),
            'strength': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 500mg'}),
            'default_dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Common dosage pattern'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PrescriptionForm(forms.ModelForm):
    """Form for creating prescriptions"""
    class Meta:
        model = Prescription
        fields = [
            'date', 'clinical_record', 'dm', 'htn', 'ihd', 'tb', 'smoking',
            'is_first_visit', 'pulse', 'spo2', 'chest_notes', 'tests_ordered',
            'special_instructions', 'follow_up'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'clinical_record': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Clinical notes and diagnosis'}),
            'dm': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'htn': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ihd': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tb': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'smoking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_first_visit': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pulse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pulse'}),
            'spo2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SPO2'}),
            'chest_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Chest examination notes'}),
            'tests_ordered': forms.CheckboxSelectMultiple(attrs={'class': 'test-checkbox'}),
            'special_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Special instructions'}),
            'follow_up': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Follow-up date/notes'}),
        }


class PrescriptionMedicineForm(forms.ModelForm):
    """Form for adding medicines to a prescription"""
    class Meta:
        model = PrescriptionMedicine
        fields = ['medicine', 'dosage', 'morning', 'afternoon', 'evening', 'night', 'days', 'instructions']
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-control medicine-select'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dosage'}),
            'morning': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'afternoon': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'evening': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'night': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'days': forms.NumberInput(attrs={'class': 'form-control days-input', 'min': 1, 'style': 'width: 70px;'}),
            'instructions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Instructions'}),
        }


# Formset for multiple medicines in a prescription
PrescriptionMedicineFormSet = forms.inlineformset_factory(
    Prescription,
    PrescriptionMedicine,
    form=PrescriptionMedicineForm,
    extra=4,
    can_delete=True
)
