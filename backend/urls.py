from django.contrib import admin
from django.urls import path , include

handler404 = 'users.views.error_404'
handler500 = 'users.views.error_500'
handler403 = 'users.views.error_403'
handler400 = 'users.views.error_400'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('users.urls')),
    path('' , include('chat.urls')),
    path('',include('documents.urls')),
]

