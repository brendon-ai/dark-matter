"""A very deep 1-dimensional fully convolutional network intended for position prediction based on raw audio waveforms, and inspired by the M34 architecture"""
# Created by Brendon Matusch, July 2018

from keras.layers import Conv1D, MaxPooling1D, Flatten, Dropout, Input, BatchNormalization, Dense, concatenate
from keras.models import Model, Sequential
from keras.regularizers import l2


def create_model() -> Model:
    """Create and return a new instance of the waveform localization network"""
    # Create a one-dimensional convolutional neural network model with rectified linear activations, using the Keras functional API
    # It should take both microphone channels and an entire clip of audio, and take the position of the bubble on all 3 axes as a secondary input
    activation = 'tanh'
    padding = 'valid'
    regularizer = l2(0.0003)
    dense_dropout = 0.5
    inputs = Input((100_000, 2))
    x = BatchNormalization()(inputs)
    x = Conv1D(
        filters=16,
        kernel_size=80,
        strides=4,
        activation=activation,
        kernel_regularizer=regularizer,
        padding=padding
    )(x)
    x = MaxPooling1D(6)(x)
    x = BatchNormalization()(x)
    for _ in range(3):
        x = Conv1D(
            filters=16,
            kernel_size=3,
            activation=activation,
            kernel_regularizer=regularizer,
            padding=padding
        )(x)
        x = BatchNormalization()(x)
    x = MaxPooling1D(6)(x)
    x = BatchNormalization()(x)
    for _ in range(4):
        x = Conv1D(
            filters=32,
            kernel_size=3,
            activation=activation,
            kernel_regularizer=regularizer,
            padding=padding
        )(x)
        x = BatchNormalization()(x)
    x = MaxPooling1D(6)(x)
    x = BatchNormalization()(x)
    for _ in range(6):
        x = Conv1D(
            filters=48,
            kernel_size=3,
            activation=activation,
            kernel_regularizer=regularizer,
            padding=padding
        )(x)
        x = BatchNormalization()(x)
    x = MaxPooling1D(6)(x)
    x = BatchNormalization()(x)
    for _ in range(3):
        x = Conv1D(
            filters=64,
            kernel_size=3,
            activation=activation,
            kernel_regularizer=regularizer,
            padding=padding
        )(x)
        x = BatchNormalization()(x)
    x = Flatten()(x)
    x = Dense(64, activation=activation, kernel_regularizer=regularizer)(x)
    x = Dropout(dense_dropout)(x)
    x = Dense(16, activation=activation, kernel_regularizer=regularizer)(x)
    x = Dropout(dense_dropout)(x)
    outputs = Dense(1, activation='sigmoid', kernel_regularizer=regularizer)(x)
    model = Model(inputs=inputs, outputs=outputs)
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