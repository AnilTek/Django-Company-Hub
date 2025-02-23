from django.db import models
from django.db.models.signals import post_save
from .file_validation import validate_file_extension
import os

# Saving document to related username folder
def upload_to_company_folder(instance, filename):
    
    employee_name = instance.employee.username if hasattr(instance, 'company') else 'default_company'
    return os.path.join(f"documents/{employee_name}", filename)


# Services Model
class Service(models.Model):
    service_name = models.CharField(max_length=255, null=True, blank=True,unique=True)

    def __str__(self):
        return self.service_name or "Unnamed Service"


# Documents Model
class Document(models.Model):
    document_name = models.CharField(max_length=255, null=True, blank=True,unique=True)

    def __str__(self):
        return self.document_name or "Unnamed Document"


# Many-to-Many Relationship Between Services and Documents
class DocumentService(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='services', null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)

    def __str__(self):
        return f"{self.document.document_name or 'Unnamed Document'} for {self.service.service_name or 'Unnamed Service'}"

from django.db import models


# Service Requests with Document Fields
class ServiceRequest(models.Model):
    company = models.ForeignKey('users.Company', on_delete=models.CASCADE, related_name='service_history', null=True, blank=True)
    employee = models.ForeignKey('users.Employee', on_delete=models.CASCADE, related_name='service_history', null=True, blank=True)
    service = models.ForeignKey('tek.Service', on_delete=models.CASCADE, related_name='request_history', null=True, blank=True)
    status = models.CharField(max_length=50, choices=[
        ('created', 'Created'),
        ('pending','Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ],default='created', null=True, blank=True)
    date_created = models.DateField(auto_now_add=True, null=True, blank=True)
    date_submitted = models.DateField(null=True, blank=True)

    # Document upload fields (8 possible documents)
    calisma_ruhsati = models.FileField(upload_to=upload_to_company_folder, validators=[validate_file_extension], null=True, blank=True)
    vergi_levhasi = models.FileField(upload_to=upload_to_company_folder, validators=[validate_file_extension], null=True, blank=True)
    ticaret_sicil_tasdiknamesi = models.FileField(upload_to=upload_to_company_folder, validators=[validate_file_extension], null=True, blank=True)
    ticaret_sicil_gazatesi = models.FileField(upload_to=upload_to_company_folder, validators=[validate_file_extension], null=True, blank=True)
    sirketin_mali_bilgileri = models.FileField(upload_to=upload_to_company_folder, validators=[validate_file_extension], null=True, blank=True)
    oda_kayit_belgesi = models.FileField(upload_to=upload_to_company_folder, validators=[validate_file_extension], null=True, blank=True)
    kurulus_sozlesmesi = models.FileField(upload_to=upload_to_company_folder, validators=[validate_file_extension], null=True, blank=True)
    imza_sirkuleri = models.FileField(upload_to=upload_to_company_folder, validators=[validate_file_extension], null=True, blank=True)
    faaliyet_belgesi = models.FileField(upload_to=upload_to_company_folder, validators=[validate_file_extension], null=True, blank=True)
    yetki_belgesi = models.FileField(upload_to=upload_to_company_folder, validators=[validate_file_extension] , null=True, blank=True)

    
    
    def delete(self, *args, **kwargs):
       
        file_fields = [
            self.kurulus_sozlesmesi,
            self.vergi_levhasi,
            self.ticaret_sicil_gazatesi,
            self.imza_sirkuleri,
            self.oda_kayit_belgesi,
            self.yetki_belgesi,
            self.faaliyet_belgesi,
            self.calisma_ruhsati,
            self.sirketin_mali_bilgileri,
            self.ticaret_sicil_tasdiknamesi,
        ]

        for file_field in file_fields:
            if file_field and os.path.isfile(file_field.path):
                os.remove(file_field.path)  

       
        super().delete(*args, **kwargs)
    def __str__(self):
        return f"{self.employee.username.upper() or 'Unnamed'} requested {self.service.service_name or 'Unnamed Service'} for {self.company.username.upper() or 'Unnamed Company'}"
    


def serviceRequestUpdate(sender, instance, created, **kwargs):
    print('Request Saved!')
    print('Instance:' , instance)
    print('Created: ' , created)

post_save.connect(serviceRequestUpdate,sender=ServiceRequest)
