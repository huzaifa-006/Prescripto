from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from .models import Patient, Medicine, Prescription, PrescriptionMedicine, LabTest
from .forms import PatientForm, MedicineForm, PrescriptionForm, PrescriptionMedicineFormSet


def home(request):
    """Home page with navigation buttons"""
    recent_patients = Patient.objects.all()[:5]
    recent_prescriptions = Prescription.objects.all()[:5]
    stats = {
        'total_patients': Patient.objects.count(),
        'total_prescriptions': Prescription.objects.count(),
        'total_medicines': Medicine.objects.filter(is_active=True).count(),
    }
    return render(request, 'clinic/home.html', {
        'recent_patients': recent_patients,
        'recent_prescriptions': recent_prescriptions,
        'stats': stats,
    })


# ============ Patient Views ============

def patient_list(request):
    """List all patients"""
    patients = Patient.objects.all()
    return render(request, 'clinic/patient_list.html', {'patients': patients})


def patient_create(request):
    """Create a new patient with duplicate detection"""
    existing_patients = []
    
    if request.method == 'POST':
        form = PatientForm(request.POST)
        
        # Check if user confirmed to create new patient despite duplicates
        confirm_new = request.POST.get('confirm_new', False)
        
        if form.is_valid():
            name = form.cleaned_data.get('name', '')
            phone = form.cleaned_data.get('phone', '')
            
            # Check for potential duplicates (by name or phone)
            if name or phone:
                query = Q()
                if name:
                    # Check for similar names (case-insensitive)
                    query |= Q(name__iexact=name) | Q(name__icontains=name)
                if phone:
                    query |= Q(phone=phone)
                
                existing_patients = Patient.objects.filter(query).distinct()[:5]
            
            # If duplicates found and user hasn't confirmed, show warning
            if existing_patients.exists() and not confirm_new:
                return render(request, 'clinic/patient_form.html', {
                    'form': form,
                    'title': 'Add New Patient',
                    'existing_patients': existing_patients,
                    'show_duplicate_warning': True,
                })
            
            # No duplicates or user confirmed - create new patient
            patient = form.save()
            messages.success(request, f'Patient {patient.name} created with ID: {patient.patient_id}')
            # Redirect to create prescription for this patient
            return redirect('prescription_create', patient_id=patient.id)
    else:
        form = PatientForm()
    return render(request, 'clinic/patient_form.html', {'form': form, 'title': 'Add New Patient'})


def patient_edit(request, pk):
    """Edit an existing patient"""
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient information updated successfully.')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'clinic/patient_form.html', {'form': form, 'title': 'Edit Patient', 'patient': patient})


def patient_detail(request, pk):
    """View patient details with prescription history"""
    patient = get_object_or_404(Patient, pk=pk)
    prescriptions = patient.prescriptions.all()
    return render(request, 'clinic/patient_detail.html', {
        'patient': patient,
        'prescriptions': prescriptions,
    })


def patient_search(request):
    """Search for patients"""
    query = request.GET.get('q', '')
    patients = []
    if query:
        patients = Patient.objects.filter(
            Q(patient_id__icontains=query) |
            Q(name__icontains=query) |
            Q(phone__icontains=query)
        )
    return render(request, 'clinic/patient_search.html', {'patients': patients, 'query': query})


# ============ Medicine Views ============

def medicine_list(request):
    """List all medicines"""
    query = request.GET.get('q', '')
    medicines = Medicine.objects.all()
    if query:
        medicines = medicines.filter(
            Q(name__icontains=query) |
            Q(form__icontains=query)
        )
    return render(request, 'clinic/medicine_list.html', {'medicines': medicines, 'query': query})


def medicine_create(request):
    """Add a new medicine"""
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            medicine = form.save()
            messages.success(request, f'Medicine "{medicine}" added successfully.')
            return redirect('medicine_list')
    else:
        form = MedicineForm()
    return render(request, 'clinic/medicine_form.html', {'form': form, 'title': 'Add New Medicine'})


def medicine_edit(request, pk):
    """Edit a medicine"""
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medicine updated successfully.')
            return redirect('medicine_list')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'clinic/medicine_form.html', {'form': form, 'title': 'Edit Medicine', 'medicine': medicine})


# ============ Prescription Views ============

def prescription_create(request, patient_id):
    """Create a prescription for a patient"""
    patient = get_object_or_404(Patient, pk=patient_id)
    lab_tests = LabTest.objects.filter(is_active=True)
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.patient = patient
            
            # Check if this is not the first visit
            if patient.prescriptions.exists():
                prescription.is_first_visit = False
            
            prescription.save()
            form.save_m2m()  # Save many-to-many relationships (tests_ordered)
            
            # Handle medicine formset
            formset = PrescriptionMedicineFormSet(request.POST, instance=prescription)
            if formset.is_valid():
                formset.save()
            
            messages.success(request, 'Prescription created successfully.')
            return redirect('prescription_detail', pk=prescription.pk)
    else:
        # Set default date to today
        from django.utils import timezone
        initial = {'date': timezone.now().date()}
        
        # Check if first visit
        if not patient.prescriptions.exists():
            initial['is_first_visit'] = True
        else:
            initial['is_first_visit'] = False
        
        form = PrescriptionForm(initial=initial)
        formset = PrescriptionMedicineFormSet()
    
    medicines = Medicine.objects.filter(is_active=True)
    
    return render(request, 'clinic/prescription_form.html', {
        'form': form,
        'formset': formset if 'formset' in dir() else PrescriptionMedicineFormSet(),
        'patient': patient,
        'medicines': medicines,
        'lab_tests': lab_tests,
        'title': 'New Prescription',
    })


def prescription_detail(request, pk):
    """View prescription details"""
    prescription = get_object_or_404(Prescription, pk=pk)
    return render(request, 'clinic/prescription_detail.html', {'prescription': prescription})


def prescription_print(request, pk):
    """Print-friendly prescription view"""
    prescription = get_object_or_404(Prescription, pk=pk)
    return render(request, 'clinic/prescription_print.html', {'prescription': prescription})


def prescription_edit(request, pk):
    """Edit an existing prescription"""
    prescription = get_object_or_404(Prescription, pk=pk)
    patient = prescription.patient
    lab_tests = LabTest.objects.filter(is_active=True)
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        formset = PrescriptionMedicineFormSet(request.POST, instance=prescription)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Prescription updated successfully.')
            return redirect('prescription_detail', pk=prescription.pk)
    else:
        form = PrescriptionForm(instance=prescription)
        formset = PrescriptionMedicineFormSet(instance=prescription)
    
    medicines = Medicine.objects.filter(is_active=True)
    
    return render(request, 'clinic/prescription_form.html', {
        'form': form,
        'formset': formset,
        'patient': patient,
        'prescription': prescription,
        'medicines': medicines,
        'lab_tests': lab_tests,
        'title': 'Edit Prescription',
    })


# ============ API Views ============

def api_medicines(request):
    """API endpoint for medicine list (for AJAX)"""
    medicines = Medicine.objects.filter(is_active=True).values('id', 'name', 'form', 'strength')
    return JsonResponse(list(medicines), safe=False)


def api_patient_search(request):
    """API endpoint for patient search (for AJAX)"""
    query = request.GET.get('q', '')
    if query:
        patients = Patient.objects.filter(
            Q(patient_id__icontains=query) |
            Q(name__icontains=query)
        ).values('id', 'patient_id', 'name', 'gender', 'age')[:10]
        return JsonResponse(list(patients), safe=False)
    return JsonResponse([], safe=False)
