from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('set_company/', views.set_company, name='set_company'),
    path('home/', views.home, name='home'),
    path('home_c/', views.home_c, name='home_c'),
    path('save_service/<int:service_id>/',views.save_service,name='save_service'),
    path('hire_req_c',views.hire_request_company,name='hire_request_company'),
    path('service_dashboard/',views.service_dashboard,name='service_dashboard'),
    path('job_offers', views.job_offer_employee, name='job_offers'), 
    #path('services_e/', views.services_e, name='services_e'), 
    path('service_history/', views.service_history, name='service_history'), 
    path('services_e_c', views.services_e_company, name='services_e_company'),
    path('man_dashboard/', views.emp_man_dashboard, name='emp_man_dashboard'), 
    path('accept_offer/<int:offer_id>/', views.accept_offer, name='accept_offer'),
    path('reject_offer/<int:offer_id>/', views.reject_offer, name='reject_offer'),
    path('new_service/<int:company_id>/', views.new_service, name='new_service'),
    path('edit_service/<int:service_id>/', views.edit_service, name='edit_service'),
    path('end_employment/<int:offer_id>/', views.end_employment, name='end_employment'),
    path('upload_document/<int:service_id>/<int:document_id>/<str:field_name>/', views.upload_document, name='upload_document'),
    path('hire_confirm/<uidb64>/<token>/', views.hire_confirm, name='hire_confirm'),
    path('emp_req/', views.send_emp_request, name='send_emp_request'),

    
]