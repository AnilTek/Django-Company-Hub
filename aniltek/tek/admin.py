from django.contrib import admin
from .models import Service, Document, DocumentService, ServiceRequest

admin.site.register(Service)
admin.site.register(Document)
admin.site.register(DocumentService)
admin.site.register(ServiceRequest)
