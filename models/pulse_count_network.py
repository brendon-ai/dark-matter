"""A fully connected neural network that is used to discriminate between neck and non-neck events based on the pulse count for each PMT"""
# Created by Brendon Matusch, August 2018

from keras.layers import Dense, BatchNormalization, InputLayer
from keras.models import Model, Sequential


def create_model() -> Model:
    """Create and return a fully connected neural network for pulse count information"""
    # Create a neural network model that includes several dense layers with hyperbolic tangent activations
    activation = 'tanh'
    model = Sequential([
        InputLayer(input_shape=(255,)),
        BatchNormalization(),
        Dense(100, activation=activation),
        Dense(40, activation=activation),
        Dense(10, activation=activation),
        Dense(1, activation='sigmoid')
    ])
    # Output a summary of the model's architecture
    print(model.summary())
    # Use a mean squared error loss function and an Adam optimizer, and print the accuracy while training
    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['accuracy']
    )
    # Return the untrained model
    return model