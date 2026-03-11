from .models import InputImagesNew

def delete_info():
    InputImagesNew.objects.all().delete()