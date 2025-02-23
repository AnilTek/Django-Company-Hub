from django.shortcuts import get_object_or_404, render,redirect
from .models import Service,Document,ServiceRequest,DocumentService
from users.models import Company,CompanyEmployee,Employee,User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now 
from django.db import models
from django.core.exceptions import ValidationError
from .file_validation import validate_file_extension
from django.views.decorators.cache import never_cache
from django.conf import settings
import datetime
from django.http import HttpResponse
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_decode
from users.tokens import account_activition_token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils import timezone

# Create your views here.




def hire_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activition_token.check_token(user, token):
        try:
            
            company_user = request.user.company
        except AttributeError:
            messages.error(request, _("This feature is only usable for companies"))
            return redirect('home')

        # Saves the employee-company instance
        company_object = CompanyEmployee(
            company=company_user,
            employee=user.employee, 
            status='approved',
            date_joined=timezone.now()
        )
        company_object.save()

        messages.success(request, _(f'{user.username} hired successfully !'))
        return redirect('emp_man_dashboard')
    else:
        messages.error(request, _('link invalid or expired !'))

    return redirect('home')




def EmpEmail(request, user, to_email):
    # structure of the mail
    mail_subject = 'İş isteği talebi'
    message = render_to_string("template_employee_hire_request.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activition_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, _('Employement request successfully sended !'))
    else:
        messages.error(request, _('an error occured while sending email !'))



@login_required(login_url='login')
def send_emp_request(request):
    if not hasattr(request.user, 'employee'):
        messages.error(request, _("This feature is only usable for employees !"))
        return redirect('home') 
    
    if request.method == 'POST':
        company_username = request.POST.get('username')

        if not company_username:
            messages.error(request, _("required a company username !"))
            return redirect('send_emp_request')

        try:
            # Şirketi al
            company = Company.objects.get(username=company_username)
        except Company.DoesNotExist:
            message = _('{company_username} named company does not exists !').format(company_username=company_username)
            messages.error(request,message)

            return redirect('send_emp_request')

        try:
            # Employee nesnesini request.user'dan al
            employee = request.user.employee
        except Employee.DoesNotExist:
            messages.error(request, _("user not an employee instance"))
            return redirect('send_emp_request')

        # E-posta gönderme
        EmpEmail(request, employee.user, company.email)
        messages.success(request, _('Job request sended successfully via E-mail'))

    return render(request, 'employment_req.html')






def set_company(request):
    if request.method == "POST":
        company_id = request.POST.get('company_id')
        if company_id:
            request.session['company_id'] = company_id
            print(f"Selected company ID: {company_id}")  
    return redirect('home') 


from django.shortcuts import render, redirect
from django.urls import reverse

def home_c(request):

    return render(request,'home.html')

def home(request, company_id=None):
   
    if not hasattr(request.user, 'employee'):
        return redirect('home_c') 


    
    company_id = request.session.get('company_id')
    print('merhaba')

    
    objectp = CompanyEmployee.objects.filter(employee=request.user.employee)
    company_object = CompanyEmployee.objects.filter(company=company_id, employee=request.user.employee)


       
    company_name = ''
    for i in company_object:
            company_name = str(i.company)
            print(f"Company Name: {company_name}")
            request.session['company_name'] = company_name
            

   
    if company_id is None:
        company_id = 0

    
    context = {
        'object': objectp,
        'company_id': company_id,
        'company_name':company_name
    }
    return render(request, 'home.html', context=context)



    



@login_required(login_url='login')
def hire_request_company(request):
    if not hasattr(request.user, 'company'):
        messages.error(request, _("Accessible only for companies ! "))
        return redirect('home')

    if request.method == 'POST':
        employee_username = request.POST.get('username')

        
        if not employee_username:
            messages.error(request, _("Employee username is required."))
            return redirect('hire_request_company')

        try:
            
            employee = Employee.objects.get(username=employee_username)
            existing_request = CompanyEmployee.objects.filter(company=request.user.company, employee=employee).first()

            if existing_request:
                message = _("{employee_name} user already got the request.").format(employee_name=employee.username)
                messages.error(request, message)
            else:
                CompanyEmployee.objects.create(
                    company=request.user.company,
                    employee=employee,
                    status='pending'
                )
                message = _("{employee_username} Job Request sended !").format(employee_username=employee.username)
                messages.success(request, message)

        except Employee.DoesNotExist:
           
            message = _("{employee_username} User not found").format(employee_username=employee_username)
            messages.error(request, message)

    return render(request, 'hire_request_company.html')




# Listing Job Offers 
@login_required(login_url='login')
def job_offer_employee(request):
    company_id = request.session.get('company_id')
    print(f'sirketin id si {company_id}')
    
    if not hasattr(request.user, 'employee'):
        messages.error(request, _("Accessible only for employees ! "))
        return redirect('home')  
    
    
    job_offers = CompanyEmployee.objects.filter(employee=request.user.employee).all()
    
    
    print('Job Offers:', job_offers)

    company_name = request.session.get('company_name')
    return render(request, 'job_offer_employee.html', {'job_offers': job_offers,'company_name':company_name})



# Accept the offer
@login_required(login_url='login')
def accept_offer(request, offer_id):

    if not hasattr(request.user, 'employee'):
        messages.error(request, _("Accessible only for employees ! "))
        return redirect('home') 

    offer = get_object_or_404(CompanyEmployee, id=offer_id)
    offer.status = 'approved'
    offer.date_joined = now()
    offer.save()
    message = _('{company_name} s offer accepted ! ').format(company_name = offer.company.name)
    messages.success(request, message)

    return redirect('job_offers')

# Reject the offer
@login_required(login_url='login')
def reject_offer(request, offer_id):

    if not hasattr(request.user, 'employee'):
        messages.error(request, _("Accessible only for employees ! "))
        return redirect('home') 



    offer = get_object_or_404(CompanyEmployee, id=offer_id)
    offer.delete()
    message = _('{company_name} s offer rejected ! ').format(company_name = offer.company.name)
    messages.error(request, message)
    return redirect('job_offers')

@login_required(login_url='login')
def end_employment(request, offer_id):

    if not hasattr(request.user, 'company'):
        messages.error(request, _("Accessible only for companies ! "))
        return redirect('home') 

    end_request = get_object_or_404(CompanyEmployee, id=offer_id)
    end_request.delete()

    message = _('{employee_name} s employment ended ').format(employee_name = end_request.employee.name)
    messages.success(request,message)
    return redirect('home')


@login_required(login_url='login')
def services_e_company(request):
    if not hasattr(request.user, 'employee'):
        messages.error(request, _("Accessible only for employees!"))
        return redirect('home')
    

    company_id = request.session.get('company_id')
    if not company_id :
        messages.error(request, _('Please select a company !'))
        return redirect('home')
    selected_company = get_object_or_404(Company, id=company_id)

    
    get_services = ServiceRequest.objects.filter(company=selected_company, employee=request.user.employee).all()

    print(f"Services for {selected_company.name}: {get_services}")
    company_name = request.session.get('company_name')
    return render(request, 'services_e_c.html', {'company': selected_company, 'services': get_services,'company_name':company_name})



@login_required(login_url='login')
def edit_service(request, service_id):
    document_status = {}
    status = {}
    required_documents = []

    selected_service_request = get_object_or_404(ServiceRequest, id=service_id)

    
    get_required_documents = DocumentService.objects.filter(
        service=selected_service_request.service
    )
    
    
    document_fields = [
        field.name.replace(" ", "_") for field in ServiceRequest._meta.get_fields()
        if isinstance(field, models.FileField)
    ]

    document_field_names = [
    field.name for field in ServiceRequest._meta.get_fields()
    if isinstance(field, models.FileField)
]

    for field_name in document_field_names:
       is_filled = bool(getattr(selected_service_request, field_name))
       document_status[field_name] = is_filled

    for k in get_required_documents:
        doc_name = str(k.document)
        fixed = doc_name.lower().replace(' ','_')
        required_documents.append(fixed)

    for i in document_status :
      for j in required_documents :
         if i == j:
             print(f'This line printed because names matched {i} == {j}')
             status[j] = document_status[i]




    print(f'Document requirements for this service: {status}')

    final_status = all(status.values())
    print(f'Final status for this service if printed "True" means this service requirements fulfilled if "False" unfulfilled ---> {final_status}')

    


    if request.method == 'POST':
         print(request.POST.get('action'))
         if request.POST.get('action') == 'delete':
            print('Merhaba')
            selected_service_request.delete()
            messages.success(request, _('Service Deleted !'))
            if hasattr(request.user, 'employee'):
                return redirect(reverse('services_e_company', current_app=request.resolver_match.namespace))
            if hasattr(request.user, 'company'):
                return redirect(reverse('service_dashboard', current_app=request.resolver_match.namespace))

    company_name = request.session.get('company_name')
    return render(request, 'edit_service.html', {
        'get_service': [selected_service_request],
        'document': get_required_documents,
        'document_fields': document_fields ,
        'document_status': document_status,
        'final_status':final_status,
        'company_name':company_name
    })






@login_required(login_url='login')
def save_service(request,service_id):
    selected_service_request = get_object_or_404(ServiceRequest, id=service_id)

    if request.method == 'POST':
         if request.POST.get('action') == 'send':
            print('Merhaba')
            selected_service_request.status = 'pending'
            selected_service_request.date_submitted = datetime.date.today()
            selected_service_request.save()
            messages.success(request, _('Service Saved !'))
            return redirect('service_history')
    return render(request,'save_service.html')







# Service History
@login_required(login_url='login')
def service_history(request):
    company_name = request.session.get('company_name')

    if hasattr(request.user, 'employee'):
        services = ServiceRequest.objects.filter(employee = request.user.employee).all()
        return render(request,'service_history.html',{'services':services,'company_name':company_name})
    
    if hasattr(request.user, 'company'):
        services = ServiceRequest.objects.filter(company = request.user.company).all()
        return render(request,'service_history.html',{'services':services})
    
    return render(request,'service_history.html')




# Upload Document
@login_required(login_url='login')
def upload_document(request, service_id, document_id, field_name):
    if not hasattr(request.user, 'employee'):
        messages.error(request, _("Accessible only for employees!"))
        return redirect('home')

    get_service = get_object_or_404(ServiceRequest, id=service_id)
    get_document = get_object_or_404(DocumentService, id=document_id)

    if request.method == 'POST':
        if request.POST.get('action') == 'clear':
            file_field = getattr(get_service, field_name)
            if file_field:
                file_field.delete(save=False) 
                setattr(get_service, field_name, None)  
                get_service.save()  
                
                message = _('{field_name} successfully cleared!').format(field_name=field_name)
                messages.success(request,message)
            else:
                 message = _('No file to clear for {field_name}.').format(field_name=field_name)
                 messages.warning(request, message)
            return redirect('upload_document', service_id=service_id, document_id=document_id, field_name=field_name)


        uploaded_file = request.FILES.get('uploaded_file')
        if uploaded_file and hasattr(get_service, field_name):
            try:
                validate_file_extension(uploaded_file)
                setattr(get_service, field_name, uploaded_file)
                get_service.save()

                message = _('{field_name} successfully uploaded!').format(field_name=field_name)
                messages.success(request,message)
                return redirect('upload_document', service_id=service_id, document_id=document_id, field_name=field_name)
            except ValidationError as e:
                messages.error(request, _(f"File validation error: {e}"))
        else:
            messages.error(request, _("Invalid file or field name!"))

    if getattr(get_service, field_name):
        is_file_uploaded = True
        file_path = getattr(get_service, field_name).url
    else:
        is_file_uploaded = False
        file_path = None

    
    company_name = request.session.get('company_name')

    return render(request, 'upload_document.html', {
        'get_service': get_service,
        'document': get_document,
        'field_name': field_name,
        'is_file_uploaded': is_file_uploaded,
        'file_path': file_path,
        'company_name':company_name
    })




# Creating New Service
@login_required(login_url='login')
def new_service(request, company_id):
    if not hasattr(request.user, 'employee'):
        messages.error(request, _("Accessible only for employees!"))
        return redirect('home')
    company_id = request.session.get('company_id')

    all_services = Service.objects.all()
    selected_company = get_object_or_404(Company, id=company_id)

    if request.method == 'POST':


        selected_service_id = request.POST.get('service')  
        print("Selected Service ID:", selected_service_id)  

        if not selected_service_id:
           return redirect('new_service', company_id=company_id)
        
        selected_service = get_object_or_404(Service, id=selected_service_id)  
        
        new_service = ServiceRequest(
            company=selected_company,
            employee=request.user.employee,
            service=selected_service
        )
        new_service.save()
        message = _('New service request for {selected_service} has been created!').format(selected_service = selected_service)
        messages.success(request,message)
        return redirect('services_e_company') 
    company_name = request.session.get('company_name')
    


    return render(request, 'new_service.html', {'services': all_services, 'company': selected_company,'company_name':company_name})





# List all the related employees
@login_required(login_url='login')
def emp_man_dashboard(request):

    if not hasattr(request.user, 'company'):
        messages.error(request, _("Accessible only for employees ! "))
        return redirect('home') 
    


    
    existing_emp = CompanyEmployee.objects.filter(company=request.user.company).all()

    print(existing_emp)

    context = {
        'object':existing_emp
    }

    return render(request,'emp_man_dashboard.html',context=context)





# List all the services instances 
@login_required(login_url='login')
def service_dashboard(request):
    if not hasattr(request.user, 'company'):
        messages.error(request, _("Accessible only for employees ! "))
        return redirect('home') 
    
    get_all_services = ServiceRequest.objects.filter(company= request.user.company).all()

    return render(request,'service_dashboard.html',{'get_all_services':get_all_services})



