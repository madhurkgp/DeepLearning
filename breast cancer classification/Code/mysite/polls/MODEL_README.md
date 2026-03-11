# Breast Cancer Model

## Model File Information

The trained breast cancer classification model (`breast-cancer-model.h5`) is 210MB and exceeds GitHub's file size limits.

## Options to Get the Model:

### Option 1: Train Your Own Model
Run the `Breast Cancer.ipynb` notebook with the local dataset to generate a new model.

### Option 2: Download from Release
The model will be available in GitHub Releases (to be uploaded separately).

### Option 3: Use Cloud Storage
The model can be downloaded from cloud storage links (to be provided).

## Model Specifications:
- **Architecture**: DenseNet201
- **Input**: 224x224 RGB images
- **Output**: Binary classification (Benign/Malignant)
- **Size**: ~210MB
- **Accuracy**: ~95% on training data

## Temporary Setup
For now, the application will need the model file to be placed manually in this location:
```
Code/mysite/polls/breast-cancer-model.h5
```
