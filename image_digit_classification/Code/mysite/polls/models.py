from django.db import models

# Create your models here.
class InputImagesNew(models.Model):
    image_id = models.AutoField(primary_key=True)
    image_name = models.CharField(default="image1", max_length=150)
    date_when_upload = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return self.image_name

    def delete(self, using=None, keep_parents=False):
        self.InputImagesNew.storage.delete(self.InputImagesNew.image_id)
        self.file.storage.delete(self.InputImagesNew.image_name)
        super().delete()