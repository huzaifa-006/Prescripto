from django.contrib import admin
from .models import Patient, Medicine, LabTest, Prescription, PrescriptionMedicine


class PrescriptionMedicineInline(admin.TabularInline):
    model = PrescriptionMedicine
    extra = 1


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'name', 'gender', 'age', 'phone', 'created_at']
    search_fields = ['patient_id', 'name', 'phone']
    list_filter = ['gender', 'created_at']
    readonly_fields = ['patient_id']


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'form', 'strength', 'is_active']
    search_fields = ['name']
    list_filter = ['form', 'is_active']


@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation', 'category', 'is_active']
    list_filter = ['category', 'is_active']


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'date', 'is_first_visit', 'created_at']
    search_fields = ['patient__name', 'patient__patient_id']
    list_filter = ['date', 'is_first_visit']
    inlines = [PrescriptionMedicineInline]


@admin.register(PrescriptionMedicine)
class PrescriptionMedicineAdmin(admin.ModelAdmin):
    list_display = ['prescription', 'medicine', 'dosage', 'days']
