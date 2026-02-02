from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Patient URLs
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/add/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:pk>/edit/', views.patient_edit, name='patient_edit'),
    path('patients/search/', views.patient_search, name='patient_search'),
    
    # Medicine URLs
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('medicines/add/', views.medicine_create, name='medicine_create'),
    path('medicines/<int:pk>/edit/', views.medicine_edit, name='medicine_edit'),
    
    # Prescription URLs
    path('prescriptions/<int:patient_id>/new/', views.prescription_create, name='prescription_create'),
    path('prescriptions/<int:pk>/', views.prescription_detail, name='prescription_detail'),
    path('prescriptions/<int:pk>/edit/', views.prescription_edit, name='prescription_edit'),
    path('prescriptions/<int:pk>/print/', views.prescription_print, name='prescription_print'),
    
    # API URLs
    path('api/medicines/', views.api_medicines, name='api_medicines'),
    path('api/patients/search/', views.api_patient_search, name='api_patient_search'),
]
