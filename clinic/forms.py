from django import forms
from .models import Patient, Medicine, Prescription, PrescriptionMedicine, LabTest


class PatientForm(forms.ModelForm):
    """Form for creating/editing patients"""
    class Meta:
        model = Patient
        fields = ['name', 'gender', 'age', 'weight']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patient Name'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight (kg)', 'step': '0.1'}),
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
            'date', 'time', 'clinical_record', 'dm', 'htn', 'ihd', 'tb', 'smoking',
            'hep_b', 'hep_c', 'obesity', 'other_history',
            'is_first_visit', 'pulse', 'spo2', 'blood_pressure', 'sugar', 'temperature',
            'respiratory_rate', 'other_vitals', 'chest_notes', 'tests_ordered',
            'instruction_avoid_food', 'instruction_no_smoking', 'instruction_gargles',
            'instruction_warm_liquids', 'other_instructions', 'counseled_in_detail',
            'rescue_rx_given', 'follow_up'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'clinical_record': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Clinical notes and diagnosis'}),
            'dm': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'htn': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ihd': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tb': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'smoking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hep_b': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hep_c': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'obesity': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'other_history': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Other medical history'}),
            'is_first_visit': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pulse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pulse'}),
            'spo2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SPO2'}),
            'blood_pressure': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blood Pressure (e.g., 120/80)'}),
            'sugar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sugar (e.g., 140 mg/dL)'}),
            'temperature': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Temperature (e.g., 98.6 F)'}),
            'respiratory_rate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Respiratory Rate (e.g., 18/min)'}),
            'other_vitals': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Other vitals'}),
            'chest_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Chest examination notes'}),
            'tests_ordered': forms.SelectMultiple(attrs={'class': 'form-control lab-tests-select', 'multiple': 'multiple'}),
            'instruction_avoid_food': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'instruction_no_smoking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'instruction_gargles': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'instruction_warm_liquids': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'other_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Additional instructions'}),
            'counseled_in_detail': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'rescue_rx_given': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'follow_up': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Follow-up date/notes'}),
        }


class PrescriptionMedicineForm(forms.ModelForm):
    """Form for adding medicines to a prescription"""
    INSTRUCTION_CHOICES = [
        ('', 'Select Instruction'),
        ('کھانے سے پہلے', 'کھانے سے پہلے (Before meal)'),
        ('کھانے کے بعد', 'کھانے کے بعد (After meal)'),
        ('سونے سے پہلے', 'سونے سے پہلے (Before sleep)'),
        ('خالی پیٹ', 'خالی پیٹ (Empty stomach)'),
        ('کھانے کے ساتھ', 'کھانے کے ساتھ (With meal)'),
        ('ضرورت کے مطابق', 'ضرورت کے مطابق (As needed)'),
        ('custom', 'Custom Instruction'),
    ]

    ENGLISH_TO_URDU = {
        'before meal': 'کھانے سے پہلے',
        'before food': 'کھانے سے پہلے',
        'after meal': 'کھانے کے بعد',
        'after food': 'کھانے کے بعد',
        'before sleep': 'سونے سے پہلے',
        'at bedtime': 'سونے سے پہلے',
        'empty stomach': 'خالی پیٹ',
        'with meal': 'کھانے کے ساتھ',
        'with food': 'کھانے کے ساتھ',
        'as needed': 'ضرورت کے مطابق',
        'prn': 'ضرورت کے مطابق',
    }

    instruction_choice = forms.ChoiceField(
        required=False,
        choices=INSTRUCTION_CHOICES,
        widget=forms.Select(
            attrs={'class': 'form-control instruction-choice-select', 'style': 'width: 100%;'}
        ),
    )
    custom_instruction = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control custom-instruction-input',
                'placeholder': 'Custom instruction',
                'style': 'width: 100%; display: none;',
            }
        ),
    )

    class Meta:
        model = PrescriptionMedicine
        fields = ['medicine', 'custom_medicine', 'dosage', 'morning', 'afternoon', 'evening', 'night', 'days', 'duration_choice', 'custom_duration', 'instructions']
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-control medicine-select'}),
            'custom_medicine': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Or type medicine name here'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dosage'}),
            'morning': forms.NumberInput(attrs={'class': 'form-control timing-input', 'min': 0, 'max': 9, 'style': 'width: 45px; text-align: center;', 'placeholder': '0'}),
            'afternoon': forms.NumberInput(attrs={'class': 'form-control timing-input', 'min': 0, 'max': 9, 'style': 'width: 45px; text-align: center;', 'placeholder': '0'}),
            'evening': forms.NumberInput(attrs={'class': 'form-control timing-input', 'min': 0, 'max': 9, 'style': 'width: 45px; text-align: center;', 'placeholder': '0'}),
            'night': forms.NumberInput(attrs={'class': 'form-control timing-input', 'min': 0, 'max': 9, 'style': 'width: 45px; text-align: center;', 'placeholder': '0'}),
            'days': forms.NumberInput(attrs={'class': 'form-control days-input', 'min': 1, 'style': 'width: 70px;'}),
            'duration_choice': forms.Select(attrs={'class': 'form-control duration-select', 'style': 'width: 100px;'}),
            'custom_duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Custom', 'style': 'width: 80px;'}),
            'instructions': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        existing_instruction = (self.initial.get('instructions') or '').strip()
        if not existing_instruction and self.instance and self.instance.pk:
            existing_instruction = (self.instance.instructions or '').strip()

        translated_instruction = self.ENGLISH_TO_URDU.get(
            existing_instruction.lower(), existing_instruction
        )
        preset_values = {
            value for value, _label in self.INSTRUCTION_CHOICES if value and value != 'custom'
        }

        if translated_instruction in preset_values:
            self.fields['instruction_choice'].initial = translated_instruction
            self.fields['custom_instruction'].initial = ''
        elif existing_instruction:
            self.fields['instruction_choice'].initial = 'custom'
            self.fields['custom_instruction'].initial = existing_instruction
        else:
            self.fields['instruction_choice'].initial = ''
            self.fields['custom_instruction'].initial = ''

        # Make all fields optional
        for field in self.fields:
            self.fields[field].required = False

    def clean(self):
        cleaned_data = super().clean()

        selected_instruction = (cleaned_data.get('instruction_choice') or '').strip()
        custom_instruction = (cleaned_data.get('custom_instruction') or '').strip()

        if selected_instruction == 'custom':
            cleaned_data['instructions'] = custom_instruction
        elif selected_instruction:
            cleaned_data['instructions'] = selected_instruction
        else:
            cleaned_data['instructions'] = ''

        return cleaned_data


# Formset for multiple medicines in a prescription
PrescriptionMedicineFormSet = forms.inlineformset_factory(
    Prescription,
    PrescriptionMedicine,
    form=PrescriptionMedicineForm,
    extra=3,
    can_delete=True
)

# Edit formset: don't add extra blank rows by default
PrescriptionMedicineEditFormSet = forms.inlineformset_factory(
    Prescription,
    PrescriptionMedicine,
    form=PrescriptionMedicineForm,
    extra=0,
    can_delete=True
)
