from django.db import models
from django.utils import timezone
import random
import string


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
        ('Cap', 'Capsule'),
        ('Syp', 'Syrup'),
        ('Inj', 'Injection'),
        ('Cream', 'Cream'),
        ('Lotion', 'Lotion'),
        ('Drops', 'Drops'),
        ('Inhaler', 'Inhaler'),
        ('Nebulizer', 'Nebulizer'),
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
    date = models.DateField(default=timezone.now)
    
    # Clinical information
    clinical_record = models.TextField(blank=True, help_text="Diagnosis and clinical notes")
    
    # Medical history checkboxes
    dm = models.BooleanField(default=False, verbose_name="DM (Diabetes)")
    htn = models.BooleanField(default=False, verbose_name="HTN (Hypertension)")
    ihd = models.BooleanField(default=False, verbose_name="IHD")
    tb = models.BooleanField(default=False, verbose_name="TB")
    smoking = models.BooleanField(default=False, verbose_name="Smoking")
    
    # Visit info
    is_first_visit = models.BooleanField(default=True)
    
    # Vital signs
    pulse = models.CharField(max_length=20, blank=True)
    spo2 = models.CharField(max_length=20, blank=True)
    chest_notes = models.TextField(blank=True)
    
    # Lab tests
    tests_ordered = models.ManyToManyField(LabTest, blank=True)
    
    # Instructions
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
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    
    # Dosage
    dosage = models.CharField(max_length=100, blank=True, help_text="e.g., 500mg")
    
    # Frequency - timing checkboxes
    morning = models.BooleanField(default=False)
    afternoon = models.BooleanField(default=False)
    evening = models.BooleanField(default=False)
    night = models.BooleanField(default=False)
    
    # Duration
    days = models.PositiveIntegerField(default=1, help_text="Number of days")
    
    # Additional instructions
    instructions = models.CharField(max_length=200, blank=True, help_text="Before/after food, etc.")
    
    def __str__(self):
        return f"{self.medicine} for {self.prescription.patient.name}"
    
    class Meta:
        ordering = ['id']
