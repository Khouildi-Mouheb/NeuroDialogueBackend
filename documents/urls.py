
from documents.views import upload_document, admin_panel
from django.urls import path
urlpatterns=[
    path('admin-panel/', admin_panel, name='admin_panel'),
    path('documents/upload/', upload_document, name='upload_document'),
    ]