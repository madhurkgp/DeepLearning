from django.urls import path
from django.conf.urls.static import static
from .views import handler, uploading

urlpatterns = [
    path('', handler, name='homepage'),
    path('upload/', uploading, name='upload'),
]