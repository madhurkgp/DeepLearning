from django.shortcuts import render, redirect
from tensorflow.keras.models import load_model
import numpy as np

from .preprocessing import imageprepare
from .forms import ImageForm
from .models import InputImagesNew
from .deleteObjects import delete_info

var = False

# delete_info()
for item in InputImagesNew.objects.all():
    print(item.image_name)


def handler(request):
    global var
    response = None
    if var:
        obj = InputImagesNew.objects.values_list('file', flat=True).order_by('-image_id')[:1]
        path_to_file = obj[0]
        print(path_to_file)
        response = predicting("polls/images/" + str(path_to_file))
        var = False
    else:
        response = "No file is selected"
    return render(request, "index.html", {'response': response})


def uploading(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            global var
            var = True
            return redirect('homepage')
    else:
        form = ImageForm()
    return render(request, 'upload.html', {'form': form})


def predicting(path_to_file):
    data = imageprepare(path_to_file)
    model = load_model('polls/baseline.h5')
    result = np.argmax(model.predict(data), axis=-1)
    return result



