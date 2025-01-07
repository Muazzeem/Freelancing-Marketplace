from django.contrib import admin
from django.urls import path,include

urlpatterns = [
     path('admin/', admin.site.urls),
     path('api/', include('freelance_app.urls')) # Register freelance_app endpoint here . so your  URL looks like this http://domain/api/...
]
