import tensorflow as tf
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.preprocessing.image import ImageDataGenerator

import datetime

def train(path, timestamp):
    print("******************************")
    print("Start Training......................")
    print(path)

    # Generate data:
    train_datagen = ImageDataGenerator(rescale=1. / 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
    training_set = train_datagen.flow_from_directory(path + "images/", target_size=(64, 64), batch_size=16, class_mode='categorical')
    print(training_set)
    nb_train_samples = len(training_set.filenames)
    print(nb_train_samples)
    num_classes = len(training_set.class_indices)
    print(num_classes)

    # Train the model:
    classifier = Sequential()
    classifier.add(Conv2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu'))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))
    classifier.add(Conv2D(32, (3, 3), activation='relu'))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))
    classifier.add(Conv2D(32, (3, 3), activation='relu'))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))
    classifier.add(Flatten())
    classifier.add(Dense(units=128, activation='relu'))
    classifier.add(Dense(units=num_classes, activation='softmax'))
    classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    classifier.fit_generator(training_set, steps_per_epoch=nb_train_samples, epochs=1)

    print(classifier.summary())
    print(training_set.class_indices)
    s = str(training_set.class_indices)
    f = open(path + 'models/' + timestamp + '-classLabel.txt', 'w')
    f.writelines(s)
    f.close()

    classifier.save(path + 'models/' + timestamp + "-keras.h5")
    print("******************************")
    print("End ****** I am watchdof10 new Training......................")
