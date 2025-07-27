
import tensorflow as tf
from tensorflow import keras

print("Loading MNIST dataset...")
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

print("Normalizing and reshaping data for CNN...")

x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0
x_train = x_train.reshape((-1, 28, 28, 1))
x_test = x_test.reshape((-1, 28, 28, 1))

print("Building the CNN model architecture...")
model = keras.Sequential([
    keras.Input(shape=(28, 28, 1)),

    keras.layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),

    keras.layers.MaxPooling2D(pool_size=(2, 2)),

    keras.layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
    keras.layers.MaxPooling2D(pool_size=(2, 2)),

    keras.layers.Flatten(),

    keras.layers.Dropout(0.5),

    keras.layers.Dense(10, activation="softmax"),
])

print("Compiling the model...")
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

print("Starting CNN model training...")
model.fit(x_train, y_train, batch_size=128, epochs=10, validation_split=0.1)

print("Evaluating the new model...")
score = model.evaluate(x_test, y_test, verbose=0)
print(f"Test loss: {score[0]}")
print(f"Test accuracy: {score[1]}")

print("Saving the new trained model...")
model.save('mnist_model.h5')

print("New CNN model training complete and saved as mnist_model.h5")