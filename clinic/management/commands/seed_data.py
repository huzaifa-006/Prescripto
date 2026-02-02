"""
Management command to seed the database with initial data for medicines and lab tests.
Run with: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from clinic.models import Medicine, LabTest


class Command(BaseCommand):
    help = 'Seeds the database with initial medicines and lab tests'

    def handle(self, *args, **options):
        self.stdout.write('Seeding medicines...')
        
        # Common medicines from the prescription template
        medicines_data = [
            # Antibiotics
            {'name': 'Acyclovir', 'form': 'Tab', 'strength': '800mg'},
            {'name': 'Acyclovir', 'form': 'Tab', 'strength': '400mg'},
            {'name': 'Amoxicillin', 'form': 'Cap', 'strength': '500mg'},
            {'name': 'Amoxicillin', 'form': 'Cap', 'strength': '250mg'},
            {'name': 'Azithromycin', 'form': 'Tab', 'strength': '500mg'},
            {'name': 'Azithromycin', 'form': 'Tab', 'strength': '250mg'},
            {'name': 'Ciprofloxacin', 'form': 'Tab', 'strength': '500mg'},
            {'name': 'Levofloxacin', 'form': 'Tab', 'strength': '500mg'},
            {'name': 'Co-Amoxiclav', 'form': 'Tab', 'strength': '625mg'},
            {'name': 'Cefixime', 'form': 'Tab', 'strength': '400mg'},
            
            # Pain relievers
            {'name': 'Panadol', 'form': 'Tab', 'strength': '500mg'},
            {'name': 'Paracetamol', 'form': 'Tab', 'strength': '500mg'},
            {'name': 'Paracetamol', 'form': 'Tab', 'strength': '650mg'},
            {'name': 'Ibuprofen', 'form': 'Tab', 'strength': '400mg'},
            {'name': 'Ibuprofen', 'form': 'Tab', 'strength': '200mg'},
            {'name': 'Diclofenac', 'form': 'Tab', 'strength': '50mg'},
            {'name': 'Naproxen', 'form': 'Tab', 'strength': '500mg'},
            
            # Respiratory
            {'name': 'Salbutamol', 'form': 'Inhaler', 'strength': '100mcg'},
            {'name': 'Budesonide', 'form': 'Inhaler', 'strength': '200mcg'},
            {'name': 'Fluticasone', 'form': 'Inhaler', 'strength': '250mcg'},
            {'name': 'Montelukast', 'form': 'Tab', 'strength': '10mg'},
            {'name': 'Theophylline', 'form': 'Tab', 'strength': '200mg'},
            {'name': 'Dextromethorphan', 'form': 'Syp', 'strength': ''},
            {'name': 'Ambroxol', 'form': 'Syp', 'strength': ''},
            {'name': 'Bromhexine', 'form': 'Syp', 'strength': ''},
            
            # Antihistamines
            {'name': 'Cetirizine', 'form': 'Tab', 'strength': '10mg'},
            {'name': 'Loratadine', 'form': 'Tab', 'strength': '10mg'},
            {'name': 'Fexofenadine', 'form': 'Tab', 'strength': '180mg'},
            {'name': 'Desloratadine', 'form': 'Tab', 'strength': '5mg'},
            {'name': 'Chlorpheniramine', 'form': 'Tab', 'strength': '4mg'},
            
            # Gastrointestinal
            {'name': 'Omeprazole', 'form': 'Cap', 'strength': '20mg'},
            {'name': 'Omeprazole', 'form': 'Cap', 'strength': '40mg'},
            {'name': 'Esomeprazole', 'form': 'Tab', 'strength': '40mg'},
            {'name': 'Pantoprazole', 'form': 'Tab', 'strength': '40mg'},
            {'name': 'Domperidone', 'form': 'Tab', 'strength': '10mg'},
            {'name': 'Metoclopramide', 'form': 'Tab', 'strength': '10mg'},
            
            # Skin/Topical
            {'name': 'Calamine', 'form': 'Lotion', 'strength': ''},
            {'name': 'Hydrocortisone', 'form': 'Cream', 'strength': '1%'},
            {'name': 'Betamethasone', 'form': 'Cream', 'strength': '0.1%'},
            {'name': 'Mupirocin', 'form': 'Cream', 'strength': '2%'},
            {'name': 'Clotrimazole', 'form': 'Cream', 'strength': '1%'},
            
            # Vitamins and supplements
            {'name': 'Vitamin C', 'form': 'Tab', 'strength': '500mg'},
            {'name': 'Vitamin D3', 'form': 'Tab', 'strength': '1000IU'},
            {'name': 'Multivitamins', 'form': 'Tab', 'strength': ''},
            {'name': 'Calcium + Vitamin D', 'form': 'Tab', 'strength': '500mg'},
            {'name': 'Zinc', 'form': 'Tab', 'strength': '20mg'},
            
            # Other common
            {'name': 'Prednisolone', 'form': 'Tab', 'strength': '5mg'},
            {'name': 'Prednisone', 'form': 'Tab', 'strength': '10mg'},
            {'name': 'Metformin', 'form': 'Tab', 'strength': '500mg'},
            {'name': 'Amlodipine', 'form': 'Tab', 'strength': '5mg'},
            {'name': 'Losartan', 'form': 'Tab', 'strength': '50mg'},
            {'name': 'Atorvastatin', 'form': 'Tab', 'strength': '10mg'},
        ]
        
        created_count = 0
        for med_data in medicines_data:
            obj, created = Medicine.objects.get_or_create(
                name=med_data['name'],
                form=med_data['form'],
                strength=med_data.get('strength', ''),
                defaults={'is_active': True}
            )
            if created:
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {created_count} medicines'))
        
        # Lab tests from prescription template
        self.stdout.write('Seeding lab tests...')
        
        lab_tests_data = [
            # Blood tests
            {'name': 'Complete Blood Count', 'abbreviation': 'CBC', 'category': 'Blood'},
            {'name': 'Erythrocyte Sedimentation Rate', 'abbreviation': 'ESR', 'category': 'Blood'},
            {'name': 'C-Reactive Protein', 'abbreviation': 'CRP', 'category': 'Blood'},
            {'name': 'Procalcitonin', 'abbreviation': 'Pro Cal', 'category': 'Blood'},
            {'name': 'Liver Function Tests', 'abbreviation': 'LFTs', 'category': 'Blood'},
            {'name': 'Renal Function Tests', 'abbreviation': 'RFTs', 'category': 'Blood'},
            {'name': 'Serum Electrolytes', 'abbreviation': 'S/E', 'category': 'Blood'},
            {'name': 'Blood Sugar Random', 'abbreviation': 'BSR', 'category': 'Blood'},
            {'name': 'Blood Sugar Fasting', 'abbreviation': 'BSF', 'category': 'Blood'},
            {'name': 'HbA1c', 'abbreviation': 'HbA1c', 'category': 'Blood'},
            {'name': 'IgE Levels', 'abbreviation': 'IgE', 'category': 'Blood'},
            {'name': 'Pro BNP', 'abbreviation': 'Pro BNP', 'category': 'Blood'},
            {'name': 'Coagulation Profile', 'abbreviation': 'Coag', 'category': 'Blood'},
            {'name': 'Hepatitis B & C Screening', 'abbreviation': 'Hep B,C', 'category': 'Blood'},
            {'name': 'Arterial Blood Gases', 'abbreviation': 'ABG', 'category': 'Blood'},
            
            # Imaging
            {'name': 'Chest X-Ray', 'abbreviation': 'CXR', 'category': 'Imaging'},
            {'name': 'X-Ray Paranasal Sinuses', 'abbreviation': 'XRAY PNS', 'category': 'Imaging'},
            {'name': 'Echocardiography', 'abbreviation': 'ECHO', 'category': 'Imaging'},
            {'name': 'Electrocardiogram', 'abbreviation': 'ECG', 'category': 'Imaging'},
            {'name': 'HRCT Chest', 'abbreviation': 'HRCT', 'category': 'Imaging'},
            {'name': 'CECT Chest', 'abbreviation': 'CECT', 'category': 'Imaging'},
            {'name': 'USG Chest', 'abbreviation': 'USG Chest', 'category': 'Imaging'},
            {'name': 'USG Abdomen', 'abbreviation': 'USG Abdomen', 'category': 'Imaging'},
            {'name': 'Pleural Fluid R/E, ADA, Cytology', 'abbreviation': 'Pleural Fluid', 'category': 'Other'},
            
            # Pulmonary
            {'name': 'Spirometry', 'abbreviation': 'Spiro', 'category': 'Pulmonary'},
            {'name': 'Bronchoscopy', 'abbreviation': 'Bronch', 'category': 'Pulmonary'},
            {'name': 'Sleep Studies', 'abbreviation': 'Sleep Study', 'category': 'Pulmonary'},
            
            # Microbiology
            {'name': 'Sputum Gram Stain', 'abbreviation': 'Sputum GS', 'category': 'Other'},
            {'name': 'Sputum C/S', 'abbreviation': 'Sputum C/S', 'category': 'Other'},
            {'name': 'Sputum Fungal (KOH) Stain', 'abbreviation': 'KOH', 'category': 'Other'},
            {'name': 'Sputum Gene XPERT', 'abbreviation': 'GeneXpert', 'category': 'Other'},
            {'name': 'AFB Smear', 'abbreviation': 'AFB', 'category': 'Other'},
            {'name': 'AFB C/S', 'abbreviation': 'AFB C/S', 'category': 'Other'},
        ]
        
        created_count = 0
        for test_data in lab_tests_data:
            obj, created = LabTest.objects.get_or_create(
                name=test_data['name'],
                defaults={
                    'abbreviation': test_data.get('abbreviation', ''),
                    'category': test_data.get('category', 'Other'),
                    'is_active': True
                }
            )
            if created:
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {created_count} lab tests'))
        self.stdout.write(self.style.SUCCESS('Database seeding completed!'))
