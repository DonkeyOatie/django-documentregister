from django.contrib import admin
from documents.models import DocumentType


class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('document_type_short', 'document_type_long', 'description')
    list_filter = ('document_type_short',)

admin.site.register(DocumentType, DocumentTypeAdmin)
