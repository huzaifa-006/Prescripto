from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Patient, Medicine, Prescription, PrescriptionMedicine, LabTest, Doctor, PrescriptionTemplate, TemplateMedicine
from .forms import (
    PatientForm,
    MedicineForm,
    PrescriptionForm,
    PrescriptionMedicineFormSet,
    PrescriptionMedicineEditFormSet,
)


# ============ Helper Utilities ============

# Curated list of common diagnoses for quick selection
COMMON_DIAGNOSES = [
    "Upper Respiratory Tract Infection (URTI)",
    "Lower Respiratory Tract Infection (LRTI)",
    "Asthma Exacerbation",
    "Chronic Obstructive Pulmonary Disease (COPD)",
    "Pneumonia",
    "Tuberculosis (TB)",
    "Acute Bronchitis",
    "Allergic Rhinitis",
    "Sinusitis",
    "Otitis Media",
    "Gastroenteritis",
    "Peptic Ulcer Disease (PUD)",
    "Gastroesophageal Reflux Disease (GERD)",
    "Urinary Tract Infection (UTI)",
    "Kidney Stone (Renal Colic)",
    "Hypertension",
    "Diabetes Mellitus",
    "Ischemic Heart Disease (IHD)",
    "Congestive Heart Failure (CHF)",
    "Migraine",
    "Tension Headache",
    "Anxiety Disorder",
    "Depressive Episode",
    "Anemia",
    "Hypothyroidism",
    "Vitamin D Deficiency",
    "COVID-19",
    "Dengue Fever",
    "Malaria",
    "Typhoid Fever",
    "Chickenpox",
    "Dermatitis",
    "Psoriasis",
    "Low Back Pain",
    "Sciatica",
    "Osteoarthritis",
    "Rheumatoid Arthritis",
    "Gout",
    "Mechanical Neck Pain",
    "Viral Fever",
    "Food Poisoning",
    "Dehydration",
    "Otitis Externa",
    "Conjunctivitis",
    "Streptococcal Pharyngitis",
]


def get_recent_diagnoses(limit=20):
    """Return up to `limit` recent unique diagnoses plus common diagnoses for quick selection."""
    # Common diagnoses list
    common_diagnoses = [
        'Acute Respiratory Infection',
        'Allergic Rhinitis',
        'Asthma',
        'Bronchitis',
        'Bronchiectasis',
        'COPD',
        'Cough - Acute',
        'Cough - Chronic',
        'Diabetes Mellitus Type 2',
        'Dyspepsia',
        'Fever',
        'Gastroesophageal Reflux Disease',
        'Headache',
        'Hypertension',
        'Influenza',
        'Laryngitis',
        'Migraine',
        'Pharyngitis',
        'Pneumonia',
        'Pulmonary Embolism',
        'Sinusitis',
        'Tuberculosis',
        'Upper Respiratory Tract Infection',
        'Viral Infection',
        'Wheeze',
    ]
    
    seen = set()
    unique_diagnoses = []
    
    # Add common diagnoses first
    for diag in common_diagnoses:
        key = diag.lower()
        seen.add(key)
        unique_diagnoses.append(diag)
    
    # Then add recent diagnoses from database
    diagnoses = Prescription.objects.exclude(diagnosis__isnull=True).exclude(diagnosis__exact='')\
        .order_by('-updated_at').values_list('diagnosis', flat=True)

    for diag in diagnoses:
        normalized = diag.strip()
        if not normalized:
            continue

        key = normalized.lower()
        if key in seen:
            continue

        seen.add(key)
        unique_diagnoses.append(normalized)

        if len(unique_diagnoses) >= limit:
            break

    return unique_diagnoses[:limit]


def get_diagnosis_options():
    """Return curated diagnoses merged with recent unique ones, no duplicates."""
    seen = set()
    options = []

    def add_diag(diag):
        key = diag.lower().strip()
        if key and key not in seen:
            seen.add(key)
            options.append(diag.strip())

    for diag in COMMON_DIAGNOSES:
        add_diag(diag)

    for diag in get_recent_diagnoses():
        add_diag(diag)

    return options


# ============ Authentication Views ============

def login_view(request):
    """Doctor login page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'clinic/login.html')


def logout_view(request):
    """Logout and redirect to login"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


def signup_view(request):
    """Doctor signup/registration page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        from django.contrib.auth.models import User
        
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        doctor_name = request.POST.get('doctor_name', '').strip()
        
        # Validation
        errors = []
        if not username:
            errors.append('Username is required.')
        elif User.objects.filter(username=username).exists():
            errors.append('Username already exists.')
        
        if not password:
            errors.append('Password is required.')
        elif len(password) < 6:
            errors.append('Password must be at least 6 characters.')
        elif password != confirm_password:
            errors.append('Passwords do not match.')
        
        if not doctor_name:
            errors.append('Doctor name is required.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            # Create user
            user = User.objects.create_user(
                username=username,
                password=password
            )
            
            # Create doctor profile
            Doctor.objects.create(
                user=user,
                name=doctor_name
            )
            
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    
    return render(request, 'clinic/signup.html')


def forgot_password_view(request):
    """Forgot password - reset by verifying doctor name"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        from django.contrib.auth.models import User
        
        username = request.POST.get('username', '').strip()
        doctor_name = request.POST.get('doctor_name', '').strip()
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        # Validation
        if not username or not doctor_name:
            messages.error(request, 'Please fill in all fields.')
        elif not new_password:
            messages.error(request, 'Please enter a new password.')
        elif len(new_password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
        elif new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            try:
                user = User.objects.get(username=username)
                # Verify doctor name matches
                if hasattr(user, 'doctor') and user.doctor.name.lower() == doctor_name.lower():
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Password reset successfully! Please login with your new password.')
                    return redirect('login')
                else:
                    messages.error(request, 'Username and Doctor Name do not match our records.')
            except User.DoesNotExist:
                messages.error(request, 'Username not found.')
    
    return render(request, 'clinic/forgot_password.html')


@login_required
def profile_view(request):
    """Doctor profile management page"""
    from django.contrib.auth import update_session_auth_hash
    
    # Get or create doctor profile
    try:
        doctor = request.user.doctor
    except Doctor.DoesNotExist:
        doctor = Doctor.objects.create(user=request.user, name=request.user.username)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_profile':
            # Update doctor profile
            doctor.name = request.POST.get('doctor_name', doctor.name)
            doctor.title = request.POST.get('title', doctor.title)
            doctor.specialization = request.POST.get('specialization', doctor.specialization)
            doctor.credentials = request.POST.get('credentials', doctor.credentials)
            doctor.contact_number = request.POST.get('contact_number', doctor.contact_number)
            doctor.hospital_name = request.POST.get('hospital_name', doctor.hospital_name)
            doctor.hospital_address = request.POST.get('hospital_address', doctor.hospital_address)
            doctor.hospital_tagline = request.POST.get('hospital_tagline', doctor.hospital_tagline)
            doctor.save()
            
            # Update user email
            new_email = request.POST.get('email', '').strip()
            if new_email and new_email != request.user.email:
                request.user.email = new_email
                request.user.save()
            
            messages.success(request, 'Profile updated successfully!')
        
        elif action == 'change_password':
            current_password = request.POST.get('current_password', '')
            new_password = request.POST.get('new_password', '')
            confirm_password = request.POST.get('confirm_new_password', '')
            
            if not request.user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
            elif len(new_password) < 6:
                messages.error(request, 'New password must be at least 6 characters.')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
            else:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password changed successfully!')
        
        return redirect('profile')
    
    return render(request, 'clinic/profile.html', {'doctor': doctor})


# ============ Dashboard View ============

@login_required
def dashboard(request):
    """Dashboard with statistics and quick actions"""
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Basic stats
    stats = {
        'total_patients': Patient.objects.count(),
        'total_prescriptions': Prescription.objects.count(),
        'total_medicines': Medicine.objects.filter(is_active=True).count(),
        'today_patients': Prescription.objects.filter(date=today).values('patient').distinct().count(),
        'today_prescriptions': Prescription.objects.filter(date=today).count(),
        'week_prescriptions': Prescription.objects.filter(date__gte=week_ago).count(),
        'month_prescriptions': Prescription.objects.filter(date__gte=month_ago).count(),
    }
    
    # Top prescribed medicines (last 30 days)
    top_medicines = PrescriptionMedicine.objects.filter(
        prescription__date__gte=month_ago
    ).exclude(medicine__isnull=True).values(
        'medicine__name', 'medicine__form'
    ).annotate(count=Count('id')).order_by('-count')[:5]
    
    # Recent patients
    recent_patients = Patient.objects.all()[:5]
    
    # Recent prescriptions
    recent_prescriptions = Prescription.objects.select_related('patient').all()[:5]
    
    # Get templates for quick access
    templates = PrescriptionTemplate.objects.filter(is_active=True)[:5]
    
    return render(request, 'clinic/dashboard.html', {
        'stats': stats,
        'top_medicines': top_medicines,
        'recent_patients': recent_patients,
        'recent_prescriptions': recent_prescriptions,
        'templates': templates,
    })


def home(request):
    """Home page - redirects to dashboard if logged in"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


# ============ Patient Views ============

@login_required
def patient_list(request):
    """List all patients"""
    patients = Patient.objects.all()
    return render(request, 'clinic/patient_list.html', {'patients': patients})


@login_required
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


@login_required
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


@login_required
def patient_detail(request, pk):
    """View patient details with prescription history"""
    patient = get_object_or_404(Patient, pk=pk)
    prescriptions = patient.prescriptions.all()
    return render(request, 'clinic/patient_detail.html', {
        'patient': patient,
        'prescriptions': prescriptions,
    })


@login_required
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

@login_required
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


@login_required
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


@login_required
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

@login_required
def prescription_create(request, patient_id):
    """Create a prescription for a patient"""
    patient = get_object_or_404(Patient, pk=patient_id)
    lab_tests = LabTest.objects.filter(is_active=True)
    templates = PrescriptionTemplate.objects.filter(is_active=True)
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        formset = PrescriptionMedicineFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            prescription = form.save(commit=False)
            prescription.patient = patient
            
            # Link to doctor if logged in and has doctor profile
            if request.user.is_authenticated:
                try:
                    prescription.doctor = request.user.doctor
                except Doctor.DoesNotExist:
                    pass
            
            # Check if this is not the first visit
            if patient.prescriptions.exists():
                prescription.is_first_visit = False
            
            prescription.save()
            form.save_m2m()  # Save many-to-many relationships (tests_ordered)
            
            # Link the formset to the prescription and process medicines
            formset.instance = prescription
            
            try:
                # Auto-save custom medicines to database for future use
                for medicine_form in formset:
                    if medicine_form.cleaned_data and not medicine_form.cleaned_data.get('DELETE', False):
                        custom_med_name = medicine_form.cleaned_data.get('custom_medicine', '').strip()
                        selected_medicine = medicine_form.cleaned_data.get('medicine')
                        
                        # If custom medicine is provided and no dropdown selection
                        if custom_med_name and not selected_medicine:
                            # Try to find existing medicine with this name
                            existing_med = Medicine.objects.filter(name__iexact=custom_med_name).first()
                            
                            if not existing_med:
                                # Create new medicine in database
                                existing_med = Medicine.objects.create(
                                    name=custom_med_name,
                                    form='Tab',  # Default form
                                    is_active=True
                                )
                            
                            # Update the form instance to link to this medicine
                            medicine_form.instance.medicine = existing_med
                            medicine_form.instance.custom_medicine = ''  # Clear custom field since we linked it
                
                formset.save()
                
                messages.success(request, 'Prescription created successfully.')
                return redirect('prescription_detail', pk=prescription.pk)
            except Exception as e:
                messages.error(request, f'Error saving medicines: {str(e)}')
                # Delete the prescription if medicine saving failed
                prescription.delete()
        else:
            # Form or formset has errors - don't save anything
            formset = PrescriptionMedicineFormSet(request.POST)
    else:
        # Set default date to today
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
        'templates': templates,
        'diagnosis_options': get_diagnosis_options(),
        'title': 'New Prescription',
    })


@login_required
def prescription_detail(request, pk):
    """View prescription details"""
    prescription = get_object_or_404(Prescription, pk=pk)
    return render(request, 'clinic/prescription_detail.html', {'prescription': prescription})


@login_required
def prescription_print(request, pk):
    """Print-friendly prescription view"""
    prescription = get_object_or_404(Prescription, pk=pk)
    return render(request, 'clinic/prescription_print.html', {'prescription': prescription})


@login_required
def prescription_edit(request, pk):
    """Edit an existing prescription"""
    prescription = get_object_or_404(Prescription, pk=pk)
    patient = prescription.patient
    lab_tests = LabTest.objects.filter(is_active=True)
    templates = PrescriptionTemplate.objects.filter(is_active=True)
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        formset = PrescriptionMedicineEditFormSet(request.POST, instance=prescription)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Prescription updated successfully.')
            return redirect('prescription_detail', pk=prescription.pk)
    else:
        form = PrescriptionForm(instance=prescription)
        formset = PrescriptionMedicineEditFormSet(instance=prescription)
    
    medicines = Medicine.objects.filter(is_active=True)
    
    return render(request, 'clinic/prescription_form.html', {
        'form': form,
        'formset': formset,
        'patient': patient,
        'prescription': prescription,
        'medicines': medicines,
        'lab_tests': lab_tests,
        'templates': templates,
        'diagnosis_options': get_diagnosis_options(),
        'title': 'Edit Prescription',
    })


@login_required
def prescription_delete(request, pk):
    """Delete a prescription"""
    prescription = get_object_or_404(Prescription, pk=pk)
    patient_id = prescription.patient.id
    
    if request.method == 'POST':
        prescription.delete()
        messages.success(request, 'Prescription deleted successfully.')
        return redirect('patient_detail', pk=patient_id)
    
    return render(request, 'clinic/prescription_confirm_delete.html', {'prescription': prescription})


@login_required
def prescription_duplicate(request, pk):
    """Duplicate an existing prescription"""
    original = get_object_or_404(Prescription, pk=pk)
    
    # Create new prescription with same data
    new_prescription = Prescription.objects.create(
        patient=original.patient,
        doctor=original.doctor,
        date=timezone.now().date(),
        clinical_record=original.clinical_record,
        dm=original.dm,
        htn=original.htn,
        ihd=original.ihd,
        tb=original.tb,
        smoking=original.smoking,
        is_first_visit=False,
        pulse=original.pulse,
        spo2=original.spo2,
        blood_pressure=original.blood_pressure,
        sugar=original.sugar,
        temperature=original.temperature,
        respiratory_rate=original.respiratory_rate,
        other_vitals=original.other_vitals,
        chest_notes=original.chest_notes,
        special_instructions=original.special_instructions,
        follow_up=original.follow_up,
    )
    
    # Copy tests ordered
    new_prescription.tests_ordered.set(original.tests_ordered.all())
    
    # Copy medicines
    for med in original.medicines.all():
        PrescriptionMedicine.objects.create(
            prescription=new_prescription,
            medicine=med.medicine,
            custom_medicine=med.custom_medicine,
            dosage=med.dosage,
            morning=med.morning,
            afternoon=med.afternoon,
            evening=med.evening,
            night=med.night,
            days=med.days,
            instructions=med.instructions,
        )
    
    messages.success(request, 'Prescription duplicated successfully. You can now edit it.')
    return redirect('prescription_edit', pk=new_prescription.pk)


# ============ Template Views ============

@login_required
def template_list(request):
    """List all prescription templates"""
    templates = PrescriptionTemplate.objects.filter(is_active=True)
    return render(request, 'clinic/template_list.html', {'templates': templates})


@login_required
def template_create(request):
    """Create a new prescription template"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        clinical_record = request.POST.get('clinical_record', '')
        special_instructions = request.POST.get('special_instructions', '')
        
        # Get doctor if exists
        doctor = None
        if request.user.is_authenticated:
            try:
                doctor = request.user.doctor
            except Doctor.DoesNotExist:
                pass
        
        template = PrescriptionTemplate.objects.create(
            name=name,
            description=description,
            doctor=doctor,
            clinical_record=clinical_record,
            special_instructions=special_instructions,
        )
        
        # Add medicines from POST data
        medicine_ids = request.POST.getlist('medicine_ids[]')
        dosages = request.POST.getlist('dosages[]')
        mornings = request.POST.getlist('mornings[]')
        afternoons = request.POST.getlist('afternoons[]')
        evenings = request.POST.getlist('evenings[]')
        nights = request.POST.getlist('nights[]')
        duration_choices = request.POST.getlist('duration_choices[]')
        custom_durations = request.POST.getlist('custom_durations[]')
        days_list = request.POST.getlist('days[]')
        
        for i, med_id in enumerate(medicine_ids):
            if med_id:
                duration_choice = duration_choices[i] if i < len(duration_choices) else ''
                custom_duration = custom_durations[i].strip() if i < len(custom_durations) else ''
                
                # Determine days based on selection; fall back to numeric days input
                days_value = 1
                if duration_choice and duration_choice != 'custom':
                    try:
                        days_value = int(duration_choice)
                    except ValueError:
                        days_value = 1
                else:
                    try:
                        days_value = int(days_list[i]) if i < len(days_list) and days_list[i] else 1
                    except (ValueError, IndexError):
                        days_value = 1
                
                TemplateMedicine.objects.create(
                    template=template,
                    medicine_id=int(med_id) if med_id else None,
                    dosage=dosages[i] if i < len(dosages) else '',
                    morning=str(i) in mornings,
                    afternoon=str(i) in afternoons,
                    evening=str(i) in evenings,
                    night=str(i) in nights,
                    days=days_value,
                    custom_duration=custom_duration if duration_choice == 'custom' else '',
                )
        
        messages.success(request, f'Template "{template.name}" created successfully.')
        return redirect('template_list')
    
    medicines = Medicine.objects.filter(is_active=True)
    return render(request, 'clinic/template_form.html', {
        'title': 'Create Template',
        'medicines': medicines,
    })


@login_required
def template_delete(request, pk):
    """Delete a template"""
    template = get_object_or_404(PrescriptionTemplate, pk=pk)
    if request.method == 'POST':
        template.delete()
        messages.success(request, 'Template deleted successfully.')
    return redirect('template_list')


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


def api_template_data(request, pk):
    """API endpoint to get template data for applying to prescription"""
    template = get_object_or_404(PrescriptionTemplate, pk=pk)
    
    data = {
        'clinical_record': template.clinical_record,
        'special_instructions': template.special_instructions,
        'medicines': []
    }
    
    for med in template.medicines.all():
        data['medicines'].append({
            'medicine_id': med.medicine.id if med.medicine else None,
            'medicine_name': med.get_medicine_name(),
            'custom_medicine': med.custom_medicine,
            'dosage': med.dosage,
            'morning': med.morning,
            'afternoon': med.afternoon,
            'evening': med.evening,
            'night': med.night,
            'days': med.days,
            'custom_duration': med.custom_duration,
            'instructions': med.instructions,
        })
    
    return JsonResponse(data)
