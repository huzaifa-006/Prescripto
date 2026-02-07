from django.urls import path
from . import views

urlpatterns = [
    # Home - redirects to dashboard or login
    path('', views.home, name='home'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('profile/', views.profile_view, name='profile'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
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
    path('prescriptions/<int:pk>/delete/', views.prescription_delete, name='prescription_delete'),
    path('prescriptions/<int:pk>/duplicate/', views.prescription_duplicate, name='prescription_duplicate'),
    
    # Template URLs
    path('templates/', views.template_list, name='template_list'),
    path('templates/create/', views.template_create, name='template_create'),
    path('templates/<int:pk>/delete/', views.template_delete, name='template_delete'),
    
    # API URLs
    path('api/medicines/', views.api_medicines, name='api_medicines'),
    path('api/patients/search/', views.api_patient_search, name='api_patient_search'),
    path('api/templates/<int:pk>/', views.api_template_data, name='api_template_data'),
]
