from transformers import pipeline
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
import numpy as np
from PIL import Image


# Real AI Models

# Text Model: Sentiment Analysis from HuggingFace
class SentimentAnalysisModel:
    def __init__(self):
        self._model = None
        self.name = "Sentiment Analyzer"
        self.category = "Text"
        self.description = "Classifies text as Positive/Negative."

    def load(self):
        if self._model is None:
            self._model = pipeline(
                "sentiment-analysis", 
                model="distilbert-base-uncased-finetuned-sst-2-english",
                framework="pt"  
            )
            return "Sentiment Analyzer loaded successfully."
        return "Sentiment Analyzer already loaded."

    def predict(self, text):
        if self._model is None:
            return "Error: Model not loaded. Press 'Load Model' first."
        if not text:
             return "Error: Please enter text for analysis."
             
        result = self._model(text)[0]
        return f"Prediction: {result['label']} (Score: {result['score']:.2f})"

# Image Model: MNIST Digit Recognition with Keras
class DigitRecognitionModel:
    def __init__(self):
        self._model = None
        self.name = "MNIST Digit Recognizer"
        self.category = "Vision"
        self.description = "Recognizes handwritten digits (0-9)."
        self.model_path = "mnist_cnn.h5"

    def load(self):
        if self._model is not None:
            return "Digit Recognizer already loaded."
            
        try:
            self._model = load_model(self.model_path)
            return "Digit Recognizer loaded from file."
        except:
            self._model = self._train_and_save_model()
            return "Digit Recognizer trained and loaded."

    def _train_and_save_model(self):
        print("Model file not found. Training a small CNN on MNIST...")
        
        # Load and preprocess data
        (x_train, y_train), (x_test, y_test) = mnist.load_data()
        x_train = x_train.reshape(-1, 28, 28, 1).astype("float32") / 255.0
        x_test = x_test.reshape(-1, 28, 28, 1).astype("float32") / 255.0
        y_train = to_categorical(y_train, 10)
        y_test = to_categorical(y_test, 10)

        # Define and compile model
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3,3), activation="relu", input_shape=(28,28,1)),
            tf.keras.layers.MaxPooling2D(2,2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(10, activation="softmax")
        ])

        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
        
        # Train model (using only 2 epochs to be quick)
        model.fit(x_train, y_train, epochs=2, validation_data=(x_test, y_test), verbose=0)
        
        # Save model
        model.save(self.model_path)
        return model

    def predict(self, image_path):
        if self._model is None:
            return "Error: Model not loaded. Press 'Load Model' first."
        if not image_path:
             return "Error: Please browse and select an image file."
             
        try:
            # Load and preprocess image (28x28 grayscale)
            img = Image.open(image_path).convert("L").resize((28, 28))
            img_array = np.array(img).reshape(1, 28, 28, 1).astype("float32") / 255.0
            
            # Predict
            pred = self._model.predict(img_array, verbose=0)
            return f"Predicted Digit: {np.argmax(pred)} (Confidence: {np.max(pred):.2f})"
        except Exception as e:
            return f"Error during prediction: {e}"