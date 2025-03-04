
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('agenda.urls')), # assim que cair no diretório api, ele vai chamar as urls da agenda
]
