// Prescripto - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
    
    // Initialize date fields with today's date if empty
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        if (!input.value) {
            const today = new Date().toISOString().split('T')[0];
            input.value = today;
        }
    });
    
    // Handle medicine selection change
    const medicineSelects = document.querySelectorAll('.medicine-select');
    medicineSelects.forEach(select => {
        select.addEventListener('change', function() {
            // Could add logic here to auto-fill dosage based on medicine
        });
    });
    
    // Real-time search for patient search page
    const searchInput = document.querySelector('.search-input');
    if (searchInput && searchInput.dataset.realtime) {
        let timeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                this.closest('form').submit();
            }, 500);
        });
    }
    
    // Print prescription
    window.printPrescription = function() {
        window.print();
    };
    
    // Confirm before deleting
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm(this.dataset.confirm || 'Are you sure?')) {
                e.preventDefault();
            }
        });
    });
    
    // Toggle delete checkboxes in formset
    const deleteChecks = document.querySelectorAll('.delete-check input');
    deleteChecks.forEach(check => {
        check.addEventListener('change', function() {
            const row = this.closest('.medicine-row');
            if (this.checked) {
                row.style.opacity = '0.5';
                row.style.textDecoration = 'line-through';
            } else {
                row.style.opacity = '1';
                row.style.textDecoration = 'none';
            }
        });
    });
});

// Function to add new medicine row in prescription form
function addMedicineRow() {
    const container = document.getElementById('medicinesTable');
    const totalForms = document.getElementById('id_medicines-TOTAL_FORMS');
    
    if (!container || !totalForms) return;
    
    const formIndex = parseInt(totalForms.value);
    const existingRow = container.querySelector('.medicine-row');
    
    if (!existingRow) return;
    
    const newRow = existingRow.cloneNode(true);
    newRow.dataset.index = formIndex;
    
    // Update all form field names and IDs
    newRow.querySelectorAll('input, select').forEach(input => {
        const name = input.name;
        const id = input.id;
        
        if (name) {
            input.name = name.replace(/-\d+-/, `-${formIndex}-`);
        }
        if (id) {
            input.id = id.replace(/-\d+-/, `-${formIndex}-`);
        }
        
        // Clear values
        if (input.type === 'checkbox') {
            input.checked = false;
        } else if (input.tagName === 'SELECT') {
            input.selectedIndex = 0;
        } else if (input.type === 'hidden' && input.name.includes('-id')) {
            input.value = '';
        } else if (input.type !== 'hidden') {
            input.value = input.name.includes('days') ? '1' : '';
        }
    });
    
    // Reset styling
    newRow.style.opacity = '1';
    newRow.style.textDecoration = 'none';
    
    container.appendChild(newRow);
    totalForms.value = formIndex + 1;
}
