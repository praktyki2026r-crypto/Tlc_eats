from django.contrib import admin
from django.urls import path, include

#glowny router, przekazuje ruch do apl przez include()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tlc_eats_app.urls')),
]