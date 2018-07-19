#!/usr/bin/env python3
"""A script for a semi-supervised training technique where certain examples have defined ground truths and others are assigned probabilistic ground truths based on what they are predicted to be by the network"""
# Created by Brendon Matusch, July 2018

import numpy as np

from data_processing.bubble_data_point import RunType
from data_processing.event_data_set import EventDataSet
from data_processing.experiment_serialization import save_test
from models.banded_frequency_network import create_model

# The number of epochs to train for
EPOCHS = 250

# The number of training examples for which the ground truth is actually used, and is not dynamically generated
DEFINITIVE_TRAINING_EXAMPLES = 512

# Create an instance of the fully connected neural network
model = create_model()

# Create a data set, running fiducial cuts for the most reasonable data
event_data_set = EventDataSet({
    RunType.LOW_BACKGROUND,
    RunType.AMERICIUM_BERYLLIUM,
    RunType.CALIFORNIUM
})
# Sort the list of training events down to only those that pass the validation cuts
event_data_set.training_events = [
    event for event in event_data_set.training_events
    if EventDataSet.passes_validation_cuts(event)
]
# Get the banded frequency domain data; the data set class will not be used from here on
training_input, training_ground_truths, validation_input, validation_ground_truths = event_data_set.banded_frequency_alpha_classification()
# Initially, set all of the training ground truths (except for the few for which the original ground truth is kept) to 0.5
# This keeps the network from learning anything it shouldn't until at least some training has been done on the definitive data
# It must first be converted to floating-point
training_ground_truths = training_ground_truths.astype(float)
training_ground_truths[DEFINITIVE_TRAINING_EXAMPLES:] = 0.5

# Iterate over however many epochs we are training for
for epoch in range(EPOCHS):
    # Train the model for one epoch
    model.fit(
        x=training_input,
        y=training_ground_truths,
        validation_data=(validation_input, validation_ground_truths),
        epochs=1
    )
    # Run predictions on the validation data set, and save the experimental run
    validation_network_outputs = model.predict(validation_input)
    save_test(
        event_data_set,
        validation_ground_truths,
        validation_network_outputs,
        epoch=epoch,
        prefix='gravitational_'
    )
