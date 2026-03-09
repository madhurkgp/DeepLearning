# Simple Convolutional Neural Network
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils

# load data
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data(
                                        path=r'C:\Users\KIIT\Desktop\Pianalytix\Code\datasets\mnist.npz')

# reshape to be [samples][width][height][channels]
X_train = X_train.reshape(X_train.shape[0], 28, 28, 1).astype('float32')
X_test = X_test.reshape(X_test.shape[0], 28, 28, 1).astype('float32')

# normalize inputs from 0-255 to 0-1
X_train = X_train / 255
X_test = X_test / 255
# one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]

def CNN_model():
	# create model
    model2 = Sequential()
    model2.add(Conv2D(32, (5, 5), input_shape=(28, 28, 1), activation='relu'))
    model2.add(MaxPooling2D(pool_size=(2, 2)))
    model2.add(Dropout(0.2))
    model2.add(Flatten())
    model2.add(Dense(128, activation='relu'))
    model2.add(Dense(num_classes, activation='softmax'))

    # Compile
    model2.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # Scaving the model
    model2.save('models/CNN-model.h5')
    return model2


# build the model
model = CNN_model()
# Fit the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200, verbose=2)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("CNN Error: %.2f%%" % (100-scores[1]*100))

# load model
# from tf.keras.models import load_model
# savedModel=load_model('models/CNN-model.h5')