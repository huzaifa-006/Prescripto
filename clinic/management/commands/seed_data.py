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
        
        # Comprehensive medicines list for pulmonology/chest specialist
        medicines_data = [
            # ============ ANTIBIOTICS ============
            {'name': 'Acyclovir', 'form': 'Tab', 'strength': '800mg'},
            {'name': 'Acyclovir', 'form': 'Tab', 'strength': '400mg'},
            {'name': 'Amoxicillin', 'form': 'Cap', 'strength': '500mg'},
            {'name': 'Amoxicillin', 'form': 'Cap', 'strength': '250mg'},
            {'name': 'Amoxicillin', 'form': 'Syp', 'strength': '125mg/5ml'},
            {'name': 'Azithromycin', 'form': 'Tab', 'strength': '500mg'},
            {'name': 'Azithromycin', 'form': 'Tab', 'strength': '250mg'},
            {'name': 'Azithromycin', 'form': 'Syp', 'strength': '200mg/5ml'},
            {'name': 'Ciprofloxacin', 'form': 'Tab', 'strength': '500mg'},
            {'name': 'Ciprofloxacin', 'form': 'Tab', 'strength': '250mg'},
            {'name': 'Levofloxacin', 'form': 'Tab', 'strength': '500mg'},
            {'name': 'Levofloxacin', 'form': 'Tab', 'strength': '750mg'},
            {'name': 'Moxifloxacin', 'form': 'Tab', 'strength': '400mg'},
            {'name': 'Co-Amoxiclav', 'form': 'Tab', 'strength': '625mg'},
            {'name': 'Co-Amoxiclav', 'form': 'Tab', 'strength': '1g'},
            {'name': 'Co-Amoxiclav', 'form': 'Syp', 'strength': '228mg/5ml'},
            {'name': 'Cefixime', 'form': 'Tab', 'strength': '400mg'},
            {'name': 'Cefixime', 'form': 'Tab', 'strength': '200mg'},
            {'name': 'Cefixime', 'form': 'Syp', 'strength': '100mg/5ml'},
            {'name': 'Cefuroxime', 'form': 'Tab', 'strength': '500mg'},
            {'name': 'Cefuroxime', 'form': 'Tab', 'strength': '250mg'},
            {'name': 'Ceftriaxone', 'form': 'Inj', 'strength': '1g'},
            {'name': 'Ceftriaxone', 'form': 'Inj', 'strength': '2g'},
            {'name': 'Cefoperazone + Sulbactam', 'form': 'Inj', 'strength': '1.5g'},
            {'name': 'Piperacillin + Tazobactam', 'form': 'Inj', 'strength': '4.5g'},
            {'name': 'Meropenem', 'form': 'Inj', 'strength': '1g'},
            {'name': 'Imipenem + Cilastatin', 'form': 'Inj', 'strength': '500mg'},
            {'name': 'Vancomycin', 'form': 'Inj', 'strength': '1g'},
            {'name': 'Linezolid', 'form': 'Tab', 'strength': '600mg'},
            {'name': 'Doxycycline', 'form': 'Cap', 'strength': '100mg'},
            {'name': 'Clarithromycin', 'form': 'Tab', 'strength': '500mg'},
            {'name': 'Clarithromycin', 'form': 'Tab', 'strength': '250mg'},
            {'name': 'Erythromycin', 'form': 'Tab', 'strength': '500mg'},
            {'name': 'Metronidazole', 'form': 'Tab', 'strength': '400mg'},
            
            # ============ COUGH & COLD MEDICINES ============
            {'name': 'Dextromethorphan', 'form': 'Syp', 'strength': '15mg/5ml'},
            {'name': 'Ambroxol', 'form': 'Syp', 'strength': '30mg/5ml'},
            {'name': 'Ambroxol', 'form': 'Tab', 'strength': '30mg'},
            {'name': 'Bromhexine', 'form': 'Syp', 'strength': '4mg/5ml'},
            {'name': 'Bromhexine', 'form': 'Tab', 'strength': '8mg'},
            {'name': 'Guaifenesin', 'form': 'Syp', 'strength': '100mg/5ml'},
            {'name': 'Acetylcysteine (NAC)', 'form': 'Sachet', 'strength': '600mg'},
            {'name': 'Acetylcysteine (NAC)', 'form': 'Tab', 'strength': '200mg'},
            {'name': 'Carbocisteine', 'form': 'Syp', 'strength': '250mg/5ml'},
            {'name': 'Carbocisteine', 'form': 'Cap', 'strength': '375mg'},
            {'name': 'Codeine Phosphate', 'form': 'Syp', 'strength': '15mg/5ml'},
            {'name': 'Pholcodine', 'form': 'Syp', 'strength': '5mg/5ml'},
            {'name': 'Levocloperastine', 'form': 'Syp', 'strength': ''},
            {'name': 'Honey Cough Syrup', 'form': 'Syp', 'strength': ''},
            {'name': 'Ivy Leaf Extract', 'form': 'Syp', 'strength': ''},
            
            # ============ FLU & FEVER MEDICINES ============
            {'name': 'Panadol', 'form': 'Tab', 'strength': '500mg'},
            {'name': 'Panadol Extra', 'form': 'Tab', 'strength': '500mg+65mg'},
            {'name': 'Panadol Cold + Flu', 'form': 'Tab', 'strength': ''},
            {'name': 'Paracetamol', 'form': 'Tab', 'strength': '500mg'},
            {'name': 'Paracetamol', 'form': 'Tab', 'strength': '650mg'},
            {'name': 'Paracetamol', 'form': 'Tab', 'strength': '1000mg'},
            {'name': 'Paracetamol', 'form': 'Syp', 'strength': '120mg/5ml'},
            {'name': 'Paracetamol', 'form': 'Syp', 'strength': '250mg/5ml'},
            {'name': 'Paracetamol', 'form': 'Drops', 'strength': '100mg/ml'},
            {'name': 'Ibuprofen', 'form': 'Tab', 'strength': '400mg'},
            {'name': 'Ibuprofen', 'form': 'Tab', 'strength': '200mg'},
            {'name': 'Ibuprofen', 'form': 'Syp', 'strength': '100mg/5ml'},
            {'name': 'Mefenamic Acid', 'form': 'Tab', 'strength': '500mg'},
            {'name': 'Mefenamic Acid', 'form': 'Syp', 'strength': '50mg/5ml'},
            {'name': 'Diclofenac', 'form': 'Tab', 'strength': '50mg'},
            {'name': 'Diclofenac', 'form': 'Tab', 'strength': '75mg SR'},
            {'name': 'Naproxen', 'form': 'Tab', 'strength': '500mg'},
            {'name': 'Naproxen', 'form': 'Tab', 'strength': '250mg'},
            {'name': 'Aspirin', 'form': 'Tab', 'strength': '75mg'},
            {'name': 'Aspirin', 'form': 'Tab', 'strength': '300mg'},
            {'name': 'Oseltamivir (Tamiflu)', 'form': 'Cap', 'strength': '75mg'},
            {'name': 'Oseltamivir (Tamiflu)', 'form': 'Syp', 'strength': '30mg/5ml'},
            
            # ============ BRONCHODILATORS & INHALERS ============
            {'name': 'Salbutamol', 'form': 'Inhaler', 'strength': '100mcg'},
            {'name': 'Salbutamol', 'form': 'Nebulizer', 'strength': '2.5mg/2.5ml'},
            {'name': 'Salbutamol', 'form': 'Tab', 'strength': '2mg'},
            {'name': 'Salbutamol', 'form': 'Syp', 'strength': '2mg/5ml'},
            {'name': 'Ipratropium Bromide', 'form': 'Nebulizer', 'strength': '500mcg/2ml'},
            {'name': 'Ipratropium + Salbutamol', 'form': 'Nebulizer', 'strength': ''},
            {'name': 'Levosalbutamol', 'form': 'Nebulizer', 'strength': '1.25mg/2.5ml'},
            {'name': 'Tiotropium', 'form': 'Inhaler', 'strength': '18mcg'},
            {'name': 'Tiotropium', 'form': 'Inhaler', 'strength': '9mcg'},
            {'name': 'Glycopyrronium', 'form': 'Inhaler', 'strength': '50mcg'},
            {'name': 'Formoterol', 'form': 'Inhaler', 'strength': '12mcg'},
            {'name': 'Salmeterol', 'form': 'Inhaler', 'strength': '50mcg'},
            {'name': 'Indacaterol', 'form': 'Inhaler', 'strength': '150mcg'},
            
            # ============ STEROIDS (INHALED) ============
            {'name': 'Budesonide', 'form': 'Inhaler', 'strength': '200mcg'},
            {'name': 'Budesonide', 'form': 'Inhaler', 'strength': '400mcg'},
            {'name': 'Budesonide', 'form': 'Nebulizer', 'strength': '0.5mg/2ml'},
            {'name': 'Budesonide', 'form': 'Nebulizer', 'strength': '1mg/2ml'},
            {'name': 'Fluticasone', 'form': 'Inhaler', 'strength': '125mcg'},
            {'name': 'Fluticasone', 'form': 'Inhaler', 'strength': '250mcg'},
            {'name': 'Fluticasone', 'form': 'Inhaler', 'strength': '500mcg'},
            {'name': 'Beclomethasone', 'form': 'Inhaler', 'strength': '100mcg'},
            {'name': 'Beclomethasone', 'form': 'Inhaler', 'strength': '250mcg'},
            {'name': 'Ciclesonide', 'form': 'Inhaler', 'strength': '160mcg'},
            {'name': 'Mometasone', 'form': 'Inhaler', 'strength': '200mcg'},
            
            # ============ COMBINATION INHALERS ============
            {'name': 'Budesonide + Formoterol', 'form': 'Inhaler', 'strength': '100/6mcg'},
            {'name': 'Budesonide + Formoterol', 'form': 'Inhaler', 'strength': '200/6mcg'},
            {'name': 'Budesonide + Formoterol', 'form': 'Inhaler', 'strength': '400/12mcg'},
            {'name': 'Fluticasone + Salmeterol', 'form': 'Inhaler', 'strength': '125/25mcg'},
            {'name': 'Fluticasone + Salmeterol', 'form': 'Inhaler', 'strength': '250/25mcg'},
            {'name': 'Fluticasone + Salmeterol', 'form': 'Inhaler', 'strength': '500/50mcg'},
            {'name': 'Fluticasone + Vilanterol', 'form': 'Inhaler', 'strength': '100/25mcg'},
            {'name': 'Fluticasone + Vilanterol', 'form': 'Inhaler', 'strength': '200/25mcg'},
            {'name': 'Tiotropium + Olodaterol', 'form': 'Inhaler', 'strength': '2.5/2.5mcg'},
            {'name': 'Umeclidinium + Vilanterol', 'form': 'Inhaler', 'strength': '62.5/25mcg'},
            
            # ============ ORAL STEROIDS ============
            {'name': 'Prednisolone', 'form': 'Tab', 'strength': '5mg'},
            {'name': 'Prednisolone', 'form': 'Tab', 'strength': '10mg'},
            {'name': 'Prednisolone', 'form': 'Tab', 'strength': '20mg'},
            {'name': 'Prednisolone', 'form': 'Syp', 'strength': '15mg/5ml'},
            {'name': 'Prednisone', 'form': 'Tab', 'strength': '5mg'},
            {'name': 'Prednisone', 'form': 'Tab', 'strength': '10mg'},
            {'name': 'Methylprednisolone', 'form': 'Tab', 'strength': '4mg'},
            {'name': 'Methylprednisolone', 'form': 'Tab', 'strength': '16mg'},
            {'name': 'Methylprednisolone', 'form': 'Inj', 'strength': '40mg'},
            {'name': 'Methylprednisolone', 'form': 'Inj', 'strength': '125mg'},
            {'name': 'Dexamethasone', 'form': 'Tab', 'strength': '0.5mg'},
            {'name': 'Dexamethasone', 'form': 'Tab', 'strength': '4mg'},
            {'name': 'Dexamethasone', 'form': 'Inj', 'strength': '4mg/ml'},
            {'name': 'Hydrocortisone', 'form': 'Inj', 'strength': '100mg'},
            
            # ============ ANTIHISTAMINES ============
            {'name': 'Cetirizine', 'form': 'Tab', 'strength': '10mg'},
            {'name': 'Cetirizine', 'form': 'Syp', 'strength': '5mg/5ml'},
            {'name': 'Levocetirizine', 'form': 'Tab', 'strength': '5mg'},
            {'name': 'Loratadine', 'form': 'Tab', 'strength': '10mg'},
            {'name': 'Loratadine', 'form': 'Syp', 'strength': '5mg/5ml'},
            {'name': 'Desloratadine', 'form': 'Tab', 'strength': '5mg'},
            {'name': 'Fexofenadine', 'form': 'Tab', 'strength': '120mg'},
            {'name': 'Fexofenadine', 'form': 'Tab', 'strength': '180mg'},
            {'name': 'Chlorpheniramine', 'form': 'Tab', 'strength': '4mg'},
            {'name': 'Chlorpheniramine', 'form': 'Syp', 'strength': '2mg/5ml'},
            {'name': 'Promethazine', 'form': 'Tab', 'strength': '25mg'},
            {'name': 'Promethazine', 'form': 'Syp', 'strength': '5mg/5ml'},
            {'name': 'Diphenhydramine', 'form': 'Syp', 'strength': '12.5mg/5ml'},
            {'name': 'Hydroxyzine', 'form': 'Tab', 'strength': '25mg'},
            {'name': 'Bilastine', 'form': 'Tab', 'strength': '20mg'},
            {'name': 'Rupatadine', 'form': 'Tab', 'strength': '10mg'},
            
            # ============ LEUKOTRIENE MODIFIERS ============
            {'name': 'Montelukast', 'form': 'Tab', 'strength': '10mg'},
            {'name': 'Montelukast', 'form': 'Tab', 'strength': '5mg (Chewable)'},
            {'name': 'Montelukast', 'form': 'Sachet', 'strength': '4mg'},
            {'name': 'Zafirlukast', 'form': 'Tab', 'strength': '20mg'},
            
            # ============ NASAL SPRAYS ============
            {'name': 'Fluticasone Nasal Spray', 'form': 'Drops', 'strength': '50mcg/spray'},
            {'name': 'Mometasone Nasal Spray', 'form': 'Drops', 'strength': '50mcg/spray'},
            {'name': 'Beclomethasone Nasal Spray', 'form': 'Drops', 'strength': '50mcg/spray'},
            {'name': 'Budesonide Nasal Spray', 'form': 'Drops', 'strength': '100mcg/spray'},
            {'name': 'Xylometazoline Nasal Drops', 'form': 'Drops', 'strength': '0.1%'},
            {'name': 'Oxymetazoline Nasal Spray', 'form': 'Drops', 'strength': '0.05%'},
            {'name': 'Normal Saline Nasal Spray', 'form': 'Drops', 'strength': '0.9%'},
            {'name': 'Azelastine Nasal Spray', 'form': 'Drops', 'strength': '0.1%'},
            
            # ============ THEOPHYLLINES ============
            {'name': 'Theophylline', 'form': 'Tab', 'strength': '200mg SR'},
            {'name': 'Theophylline', 'form': 'Tab', 'strength': '300mg SR'},
            {'name': 'Aminophylline', 'form': 'Tab', 'strength': '100mg'},
            {'name': 'Aminophylline', 'form': 'Inj', 'strength': '250mg'},
            {'name': 'Doxofylline', 'form': 'Tab', 'strength': '400mg'},
            {'name': 'Doxofylline', 'form': 'Tab', 'strength': '200mg'},
            {'name': 'Acebrophylline', 'form': 'Tab', 'strength': '100mg'},
            
            # ============ ANTI-TB MEDICINES ============
            {'name': 'Isoniazid (INH)', 'form': 'Tab', 'strength': '300mg'},
            {'name': 'Rifampicin', 'form': 'Cap', 'strength': '450mg'},
            {'name': 'Rifampicin', 'form': 'Cap', 'strength': '600mg'},
            {'name': 'Pyrazinamide', 'form': 'Tab', 'strength': '500mg'},
            {'name': 'Ethambutol', 'form': 'Tab', 'strength': '400mg'},
            {'name': 'Streptomycin', 'form': 'Inj', 'strength': '1g'},
            {'name': 'RHZE (4 FDC)', 'form': 'Tab', 'strength': ''},
            {'name': 'RHE (3 FDC)', 'form': 'Tab', 'strength': ''},
            {'name': 'Pyridoxine (Vitamin B6)', 'form': 'Tab', 'strength': '50mg'},
            {'name': 'Bedaquiline', 'form': 'Tab', 'strength': '100mg'},
            {'name': 'Delamanid', 'form': 'Tab', 'strength': '50mg'},
            
            # ============ GASTROINTESTINAL ============
            {'name': 'Omeprazole', 'form': 'Cap', 'strength': '20mg'},
            {'name': 'Omeprazole', 'form': 'Cap', 'strength': '40mg'},
            {'name': 'Esomeprazole', 'form': 'Tab', 'strength': '20mg'},
            {'name': 'Esomeprazole', 'form': 'Tab', 'strength': '40mg'},
            {'name': 'Pantoprazole', 'form': 'Tab', 'strength': '40mg'},
            {'name': 'Lansoprazole', 'form': 'Cap', 'strength': '30mg'},
            {'name': 'Rabeprazole', 'form': 'Tab', 'strength': '20mg'},
            {'name': 'Ranitidine', 'form': 'Tab', 'strength': '150mg'},
            {'name': 'Famotidine', 'form': 'Tab', 'strength': '40mg'},
            {'name': 'Domperidone', 'form': 'Tab', 'strength': '10mg'},
            {'name': 'Metoclopramide', 'form': 'Tab', 'strength': '10mg'},
            {'name': 'Ondansetron', 'form': 'Tab', 'strength': '4mg'},
            {'name': 'Ondansetron', 'form': 'Tab', 'strength': '8mg'},
            {'name': 'Antacid Syrup', 'form': 'Syp', 'strength': ''},
            
            # ============ VITAMINS & SUPPLEMENTS ============
            {'name': 'Vitamin C', 'form': 'Tab', 'strength': '500mg'},
            {'name': 'Vitamin C', 'form': 'Tab', 'strength': '1000mg'},
            {'name': 'Vitamin D3', 'form': 'Tab', 'strength': '1000IU'},
            {'name': 'Vitamin D3', 'form': 'Tab', 'strength': '2000IU'},
            {'name': 'Vitamin D3', 'form': 'Sachet', 'strength': '200000IU'},
            {'name': 'Multivitamins', 'form': 'Tab', 'strength': ''},
            {'name': 'Calcium + Vitamin D', 'form': 'Tab', 'strength': '500mg+200IU'},
            {'name': 'Zinc', 'form': 'Tab', 'strength': '20mg'},
            {'name': 'Zinc', 'form': 'Tab', 'strength': '50mg'},
            {'name': 'Vitamin B Complex', 'form': 'Tab', 'strength': ''},
            {'name': 'Iron + Folic Acid', 'form': 'Tab', 'strength': ''},
            {'name': 'Vitamin E', 'form': 'Cap', 'strength': '400IU'},
            
            # ============ CARDIAC MEDICINES ============
            {'name': 'Amlodipine', 'form': 'Tab', 'strength': '5mg'},
            {'name': 'Amlodipine', 'form': 'Tab', 'strength': '10mg'},
            {'name': 'Losartan', 'form': 'Tab', 'strength': '50mg'},
            {'name': 'Losartan', 'form': 'Tab', 'strength': '100mg'},
            {'name': 'Telmisartan', 'form': 'Tab', 'strength': '40mg'},
            {'name': 'Telmisartan', 'form': 'Tab', 'strength': '80mg'},
            {'name': 'Enalapril', 'form': 'Tab', 'strength': '5mg'},
            {'name': 'Ramipril', 'form': 'Tab', 'strength': '5mg'},
            {'name': 'Metoprolol', 'form': 'Tab', 'strength': '50mg'},
            {'name': 'Bisoprolol', 'form': 'Tab', 'strength': '5mg'},
            {'name': 'Atenolol', 'form': 'Tab', 'strength': '50mg'},
            {'name': 'Carvedilol', 'form': 'Tab', 'strength': '6.25mg'},
            {'name': 'Furosemide', 'form': 'Tab', 'strength': '40mg'},
            {'name': 'Furosemide', 'form': 'Inj', 'strength': '20mg'},
            {'name': 'Spironolactone', 'form': 'Tab', 'strength': '25mg'},
            {'name': 'Atorvastatin', 'form': 'Tab', 'strength': '10mg'},
            {'name': 'Atorvastatin', 'form': 'Tab', 'strength': '20mg'},
            {'name': 'Rosuvastatin', 'form': 'Tab', 'strength': '10mg'},
            {'name': 'Clopidogrel', 'form': 'Tab', 'strength': '75mg'},
            {'name': 'Digoxin', 'form': 'Tab', 'strength': '0.25mg'},
            {'name': 'Diltiazem', 'form': 'Tab', 'strength': '30mg'},
            
            # ============ DIABETES MEDICINES ============
            {'name': 'Metformin', 'form': 'Tab', 'strength': '500mg'},
            {'name': 'Metformin', 'form': 'Tab', 'strength': '850mg'},
            {'name': 'Metformin', 'form': 'Tab', 'strength': '1000mg'},
            {'name': 'Glimepiride', 'form': 'Tab', 'strength': '2mg'},
            {'name': 'Glimepiride', 'form': 'Tab', 'strength': '4mg'},
            {'name': 'Gliclazide', 'form': 'Tab', 'strength': '80mg'},
            {'name': 'Sitagliptin', 'form': 'Tab', 'strength': '100mg'},
            {'name': 'Empagliflozin', 'form': 'Tab', 'strength': '25mg'},
            {'name': 'Dapagliflozin', 'form': 'Tab', 'strength': '10mg'},
            {'name': 'Human Insulin 70/30', 'form': 'Inj', 'strength': '100IU/ml'},
            
            # ============ PAIN & MUSCLE RELAXANTS ============
            {'name': 'Tramadol', 'form': 'Cap', 'strength': '50mg'},
            {'name': 'Tramadol', 'form': 'Inj', 'strength': '50mg'},
            {'name': 'Baclofen', 'form': 'Tab', 'strength': '10mg'},
            {'name': 'Tizanidine', 'form': 'Tab', 'strength': '2mg'},
            {'name': 'Orphenadrine', 'form': 'Tab', 'strength': '100mg'},
            {'name': 'Etoricoxib', 'form': 'Tab', 'strength': '90mg'},
            {'name': 'Celecoxib', 'form': 'Cap', 'strength': '200mg'},
            
            # ============ ANTIFUNGALS ============
            {'name': 'Fluconazole', 'form': 'Tab', 'strength': '150mg'},
            {'name': 'Fluconazole', 'form': 'Tab', 'strength': '200mg'},
            {'name': 'Itraconazole', 'form': 'Cap', 'strength': '100mg'},
            {'name': 'Voriconazole', 'form': 'Tab', 'strength': '200mg'},
            {'name': 'Amphotericin B', 'form': 'Inj', 'strength': '50mg'},
            {'name': 'Clotrimazole', 'form': 'Cream', 'strength': '1%'},
            
            # ============ ANTIPARASITICS ============
            {'name': 'Ivermectin', 'form': 'Tab', 'strength': '12mg'},
            {'name': 'Albendazole', 'form': 'Tab', 'strength': '400mg'},
            {'name': 'Mebendazole', 'form': 'Tab', 'strength': '100mg'},
            
            # ============ MISCELLANEOUS ============
            {'name': 'Sildenafil', 'form': 'Tab', 'strength': '20mg'},
            {'name': 'Tadalafil', 'form': 'Tab', 'strength': '10mg'},
            {'name': 'Bosentan', 'form': 'Tab', 'strength': '62.5mg'},
            {'name': 'Pirfenidone', 'form': 'Tab', 'strength': '200mg'},
            {'name': 'Nintedanib', 'form': 'Cap', 'strength': '150mg'},
            {'name': 'N-Acetylcysteine', 'form': 'Sachet', 'strength': '600mg'},
            {'name': 'Roflumilast', 'form': 'Tab', 'strength': '500mcg'},
            {'name': 'Alprazolam', 'form': 'Tab', 'strength': '0.5mg'},
            {'name': 'Clonazepam', 'form': 'Tab', 'strength': '0.5mg'},
            {'name': 'Pregabalin', 'form': 'Cap', 'strength': '75mg'},
            {'name': 'Gabapentin', 'form': 'Cap', 'strength': '300mg'},
            {'name': 'Amitriptyline', 'form': 'Tab', 'strength': '25mg'},
            {'name': 'ORS (Oral Rehydration Salts)', 'form': 'Sachet', 'strength': ''},
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
        
        # Lab tests for pulmonology practice
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
            {'name': 'D-Dimer', 'abbreviation': 'D-Dimer', 'category': 'Blood'},
            {'name': 'Troponin I', 'abbreviation': 'Trop I', 'category': 'Blood'},
            {'name': 'Lipid Profile', 'abbreviation': 'Lipids', 'category': 'Blood'},
            {'name': 'Thyroid Function Tests', 'abbreviation': 'TFTs', 'category': 'Blood'},
            {'name': 'Uric Acid', 'abbreviation': 'Uric Acid', 'category': 'Blood'},
            {'name': 'Vitamin D Level', 'abbreviation': 'Vit D', 'category': 'Blood'},
            {'name': 'Serum Ferritin', 'abbreviation': 'Ferritin', 'category': 'Blood'},
            {'name': 'LDH', 'abbreviation': 'LDH', 'category': 'Blood'},
            {'name': 'ANA', 'abbreviation': 'ANA', 'category': 'Blood'},
            {'name': 'Anti-CCP', 'abbreviation': 'Anti-CCP', 'category': 'Blood'},
            {'name': 'Rheumatoid Factor', 'abbreviation': 'RF', 'category': 'Blood'},
            {'name': 'HIV Screening', 'abbreviation': 'HIV', 'category': 'Blood'},
            {'name': 'Blood Culture', 'abbreviation': 'Blood C/S', 'category': 'Blood'},
            
            # Imaging
            {'name': 'Chest X-Ray', 'abbreviation': 'CXR', 'category': 'Imaging'},
            {'name': 'Chest X-Ray PA View', 'abbreviation': 'CXR PA', 'category': 'Imaging'},
            {'name': 'Chest X-Ray Lateral', 'abbreviation': 'CXR Lat', 'category': 'Imaging'},
            {'name': 'X-Ray Paranasal Sinuses', 'abbreviation': 'XRAY PNS', 'category': 'Imaging'},
            {'name': 'X-Ray Neck Soft Tissue', 'abbreviation': 'XRAY Neck', 'category': 'Imaging'},
            {'name': 'Echocardiography', 'abbreviation': 'ECHO', 'category': 'Imaging'},
            {'name': 'Electrocardiogram', 'abbreviation': 'ECG', 'category': 'Imaging'},
            {'name': 'HRCT Chest', 'abbreviation': 'HRCT', 'category': 'Imaging'},
            {'name': 'CECT Chest', 'abbreviation': 'CECT', 'category': 'Imaging'},
            {'name': 'CT Pulmonary Angiography', 'abbreviation': 'CTPA', 'category': 'Imaging'},
            {'name': 'CT Paranasal Sinuses', 'abbreviation': 'CT PNS', 'category': 'Imaging'},
            {'name': 'USG Chest', 'abbreviation': 'USG Chest', 'category': 'Imaging'},
            {'name': 'USG Abdomen', 'abbreviation': 'USG Abdomen', 'category': 'Imaging'},
            {'name': 'MRI Chest', 'abbreviation': 'MRI Chest', 'category': 'Imaging'},
            {'name': 'PET Scan', 'abbreviation': 'PET', 'category': 'Imaging'},
            {'name': 'V/Q Scan', 'abbreviation': 'V/Q', 'category': 'Imaging'},
            
            # Pulmonary Function & Procedures
            {'name': 'Spirometry', 'abbreviation': 'Spiro', 'category': 'Pulmonary'},
            {'name': 'Full Pulmonary Function Test', 'abbreviation': 'Full PFT', 'category': 'Pulmonary'},
            {'name': 'DLCO', 'abbreviation': 'DLCO', 'category': 'Pulmonary'},
            {'name': '6 Minute Walk Test', 'abbreviation': '6MWT', 'category': 'Pulmonary'},
            {'name': 'Bronchoscopy', 'abbreviation': 'Bronch', 'category': 'Pulmonary'},
            {'name': 'Bronchoalveolar Lavage', 'abbreviation': 'BAL', 'category': 'Pulmonary'},
            {'name': 'Sleep Studies / Polysomnography', 'abbreviation': 'PSG', 'category': 'Pulmonary'},
            {'name': 'Peak Flow Meter Reading', 'abbreviation': 'PEFR', 'category': 'Pulmonary'},
            {'name': 'Pulse Oximetry', 'abbreviation': 'SpO2', 'category': 'Pulmonary'},
            {'name': 'Thoracentesis', 'abbreviation': 'Thoraco', 'category': 'Pulmonary'},
            {'name': 'Pleural Biopsy', 'abbreviation': 'Pl Biopsy', 'category': 'Pulmonary'},
            
            # Microbiology & Special Tests
            {'name': 'Sputum Gram Stain', 'abbreviation': 'Sputum GS', 'category': 'Other'},
            {'name': 'Sputum Culture & Sensitivity', 'abbreviation': 'Sputum C/S', 'category': 'Other'},
            {'name': 'Sputum Fungal (KOH) Stain', 'abbreviation': 'KOH', 'category': 'Other'},
            {'name': 'Sputum Gene XPERT', 'abbreviation': 'GeneXpert', 'category': 'Other'},
            {'name': 'AFB Smear', 'abbreviation': 'AFB', 'category': 'Other'},
            {'name': 'AFB Culture & Sensitivity', 'abbreviation': 'AFB C/S', 'category': 'Other'},
            {'name': 'Mantoux Test', 'abbreviation': 'Mantoux', 'category': 'Other'},
            {'name': 'Quantiferon TB Gold', 'abbreviation': 'QFT-Gold', 'category': 'Other'},
            {'name': 'Pleural Fluid R/E', 'abbreviation': 'Pl Fluid R/E', 'category': 'Other'},
            {'name': 'Pleural Fluid ADA', 'abbreviation': 'Pl Fluid ADA', 'category': 'Other'},
            {'name': 'Pleural Fluid Cytology', 'abbreviation': 'Pl Cytology', 'category': 'Other'},
            {'name': 'Pleural Fluid Gene XPERT', 'abbreviation': 'Pl GeneXpert', 'category': 'Other'},
            {'name': 'Nasal Swab for COVID-19', 'abbreviation': 'COVID PCR', 'category': 'Other'},
            {'name': 'COVID-19 Rapid Antigen', 'abbreviation': 'RAT', 'category': 'Other'},
            {'name': 'Influenza A/B PCR', 'abbreviation': 'Flu PCR', 'category': 'Other'},
            {'name': 'Respiratory Viral Panel', 'abbreviation': 'RVP', 'category': 'Other'},
            {'name': 'Allergy Skin Prick Test', 'abbreviation': 'SPT', 'category': 'Other'},
            {'name': 'Specific IgE Panel', 'abbreviation': 'Spec IgE', 'category': 'Other'},
            {'name': 'Urine Routine Examination', 'abbreviation': 'Urine R/E', 'category': 'Other'},
            {'name': 'Stool Routine Examination', 'abbreviation': 'Stool R/E', 'category': 'Other'},
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
