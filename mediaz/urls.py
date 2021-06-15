from django.conf import settings #added
from django.conf.urls.static import static #added
from django.urls import path, include

urlpatterns = [
    path('', include ('upload.urls')),
    path('', include ('login_app.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
