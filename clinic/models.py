from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string

def get_current_local_date():
    return timezone.localtime(timezone.now()).date()

def get_current_local_time():
    return timezone.localtime(timezone.now()).time()

class Doctor(models.Model):
    """Doctor profile linked to Django User"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=100, blank=True, help_text="e.g., Assistant Professor")
    credentials = models.TextField(blank=True, help_text="e.g., M.B.B.S, F.C.P.S")
    specialization = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Hospital/Clinic info
    hospital_name = models.CharField(max_length=200, blank=True)
    hospital_address = models.TextField(blank=True)
    hospital_tagline = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"Dr. {self.name}"


class Patient(models.Model):
    """Patient model with unique ID"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    patient_id = models.CharField(max_length=10, unique=True, editable=False)
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.patient_id:
            # Generate unique patient ID: PT-XXXXX
            while True:
                random_id = ''.join(random.choices(string.digits, k=5))
                patient_id = f'PT-{random_id}'
                if not Patient.objects.filter(patient_id=patient_id).exists():
                    self.patient_id = patient_id
                    break
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.patient_id} - {self.name}"
    
    class Meta:
        ordering = ['-created_at']


class Medicine(models.Model):
    """Medicine database"""
    FORM_CHOICES = [
        ('Tab', 'Tablet'),
        ('Dispersible Tablet', 'Dispersible Tablet'),
        ('Cap', 'Capsule'),
        ('Syp', 'Syrup'),
        ('Inj', 'Injection'),
        ('Nasal Spray', 'Nasal Spray'),
        ('Cream', 'Cream'),
        ('Gel', 'Gel'),
        ('Ointment', 'Ointment'),
        ('Lotion', 'Lotion'),
        ('Drops', 'Drops'),
        ('Inhaler', 'Inhaler'),
        ('Nebulizer', 'Nebulizer'),
        ('Nebulizer Solution', 'Nebulizer Solution'),
        ('Sachet', 'Sachet'),
    ]
    
    name = models.CharField(max_length=200)
    form = models.CharField(max_length=20, choices=FORM_CHOICES, default='Tab')
    strength = models.CharField(max_length=50, blank=True, help_text="e.g., 500mg, 250ml")
    default_dosage = models.CharField(max_length=100, blank=True, help_text="Common dosage pattern")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        display = f"{self.form} {self.name}"
        if self.strength:
            display += f" {self.strength}"
        return display
    
    class Meta:
        ordering = ['name']
        unique_together = ['name', 'form', 'strength']


class LabTest(models.Model):
    """Lab tests that can be ordered"""
    CATEGORY_CHOICES = [
        ('Blood', 'Blood Tests'),
        ('Imaging', 'Imaging'),
        ('Pulmonary', 'Pulmonary Function'),
        ('Other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Blood')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        if self.abbreviation:
            return f"{self.abbreviation} ({self.name})"
        return self.name
    
    class Meta:
        ordering = ['category', 'name']


class Prescription(models.Model):
    """Prescription record for a patient"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='prescriptions')
    date = models.DateField(default=get_current_local_date)
    time = models.TimeField(default=get_current_local_time, blank=True, null=True)
    
    # Clinical information
    clinical_record = models.TextField(blank=True, help_text="Diagnosis and clinical notes")
    
    # Medical history checkboxes
    dm = models.BooleanField(default=False, verbose_name="DM (Diabetes)")
    htn = models.BooleanField(default=False, verbose_name="HTN (Hypertension)")
    ihd = models.BooleanField(default=False, verbose_name="IHD")
    tb = models.BooleanField(default=False, verbose_name="TB")
    smoking = models.BooleanField(default=False, verbose_name="Smoking")
    hep_b = models.BooleanField(default=False, verbose_name="Hep-B")
    hep_c = models.BooleanField(default=False, verbose_name="Hep-C")
    obesity = models.BooleanField(default=False, verbose_name="Obesity")
    other_history = models.CharField(max_length=200, blank=True, help_text="Other medical history notes")
    
    # Visit info
    is_first_visit = models.BooleanField(default=True)
    
    # Vital signs
    pulse = models.CharField(max_length=20, blank=True)
    spo2 = models.CharField(max_length=20, blank=True)
    blood_pressure = models.CharField(max_length=30, blank=True, help_text="e.g., 120/80")
    sugar = models.CharField(max_length=30, blank=True, help_text="e.g., 140 mg/dL")
    temperature = models.CharField(max_length=20, blank=True, help_text="e.g., 98.6 F")
    respiratory_rate = models.CharField(max_length=20, blank=True, help_text="e.g., 18/min")
    other_vitals = models.TextField(blank=True, help_text="Any additional vital notes")
    chest_notes = models.TextField(blank=True)
    
    # Lab tests
    tests_ordered = models.ManyToManyField(LabTest, blank=True)
    
    # Predefined instructions (checkboxes)
    instruction_avoid_food = models.BooleanField(default=False, verbose_name="Avoid Citrus, Fried, Cold and Junk food items")
    instruction_no_smoking = models.BooleanField(default=False, verbose_name="Smoking, Cold drinks strongly prohibited")
    instruction_gargles = models.BooleanField(default=False, verbose_name="Gargles after any type of inhaler are mandatory")
    instruction_warm_liquids = models.BooleanField(default=False, verbose_name="Use warm liquids frequently")
    
    # Other instructions (text field for custom instructions)
    other_instructions = models.TextField(blank=True, help_text="Additional custom instructions")
    
    # Counseled in detail checkbox
    counseled_in_detail = models.BooleanField(default=False, verbose_name="Counseled in detail")
    
    # Rescue Rx checkbox
    rescue_rx_given = models.BooleanField(default=False, verbose_name="Rescue Rx given with IV Steroid and Nebulization")
    
    # Legacy field (keep for backward compatibility)
    special_instructions = models.TextField(blank=True)
    follow_up = models.CharField(max_length=100, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Prescription for {self.patient.name} on {self.date}"
    
    class Meta:
        ordering = ['-date', '-created_at']


class PrescriptionMedicine(models.Model):
    """Medicines prescribed in a prescription with dosage details"""
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='medicines')
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT, null=True, blank=True)
    
    # Custom medicine name (if not selecting from dropdown)
    custom_medicine = models.CharField(max_length=200, blank=True, help_text="Type medicine name if not in list")
    
    # Dosage
    dosage = models.CharField(max_length=100, blank=True, help_text="e.g., 500mg")
    
    # Frequency - timing (number of tablets/doses)
    morning = models.PositiveIntegerField(default=0, help_text="Number of tablets in morning")
    afternoon = models.PositiveIntegerField(default=0, help_text="Number of tablets in afternoon")
    evening = models.PositiveIntegerField(default=0, help_text="Number of tablets in evening")
    night = models.PositiveIntegerField(default=0, help_text="Number of tablets at night")
    
    # Duration
    days = models.PositiveIntegerField(default=1, help_text="Number of days")
    
    # Duration presets
    DURATION_CHOICES = [
        ('', 'Select Duration'),
        ('1week', '1 Week'),
        ('2weeks', '2 Weeks'),
        ('1month', '1 Month'),
        ('2months', '2 Months'),
        ('custom', 'Custom'),
    ]
    duration_choice = models.CharField(max_length=20, choices=DURATION_CHOICES, blank=True, default='')
    custom_duration = models.CharField(max_length=50, blank=True, help_text="Custom duration text")
    
    # Additional instructions
    instructions = models.CharField(max_length=200, blank=True, help_text="Before/after food, etc.")

    INSTRUCTION_TRANSLATIONS = {
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
    
    def get_medicine_name(self):
        """Returns medicine name (from dropdown or custom text)"""
        if self.medicine:
            return str(self.medicine)
        return self.custom_medicine or "Unknown"

    def get_instruction_display_text(self):
        instruction = (self.instructions or "").strip()
        if not instruction:
            return "-"

        return self.INSTRUCTION_TRANSLATIONS.get(instruction.lower(), instruction)
    
    def __str__(self):
        return f"{self.get_medicine_name()} for {self.prescription.patient.name}"
    
    class Meta:
        ordering = ['id']


class PrescriptionTemplate(models.Model):
    """Reusable prescription template for common conditions"""
    name = models.CharField(max_length=200, help_text="e.g., Asthma Standard Treatment")
    description = models.TextField(blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True, related_name='templates')
    clinical_record = models.TextField(blank=True, help_text="Default diagnosis notes")
    special_instructions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class TemplateMedicine(models.Model):
    """Medicines in a prescription template"""
    template = models.ForeignKey(PrescriptionTemplate, on_delete=models.CASCADE, related_name='medicines')
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT, null=True, blank=True)
    custom_medicine = models.CharField(max_length=200, blank=True)
    dosage = models.CharField(max_length=100, blank=True)
    morning = models.BooleanField(default=False)
    afternoon = models.BooleanField(default=False)
    evening = models.BooleanField(default=False)
    night = models.BooleanField(default=False)
    days = models.PositiveIntegerField(default=1)
    instructions = models.CharField(max_length=200, blank=True)
    
    def get_medicine_name(self):
        if self.medicine:
            return str(self.medicine)
        return self.custom_medicine or "Unknown"
    
    def __str__(self):
        return f"{self.get_medicine_name()} in {self.template.name}"
    
    class Meta:
        ordering = ['id']
