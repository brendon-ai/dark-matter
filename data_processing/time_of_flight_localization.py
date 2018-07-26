"""Code for localizing the position of bubbles based on the times of arrival of the signal at multiple piezos"""
# Created by Brendon Matusch, July 2018

import autograd.numpy as np
from autograd import grad
from scipy.optimize import minimize

# A list of the positions of the piezos in 3D space, using the same units as the bubble positions in the ROOT file
PIEZO_POSITIONS = [
    np.array([5, 5, 0]),
    np.array([-5, -5, 0]),
    np.array([3, -3, 0]),
    np.array([-3, 3, 0])
]

# The speed of sound, in distance units per second, in the medium present in the vessel
SPEED_OF_SOUND = 1


def expected_times_of_flight(bubble_position):
    """Calculate the expected times of flight, from a bubble at a certain point to each of the piezos"""
    # Create a list to hold the expected times of flight
    times_of_flight = []
    # Iterate over each of the piezo positions
    for piezo_position in PIEZO_POSITIONS:
        # Calculate the distance between this piezo and the bubble
        distance = np.linalg.norm(bubble_position - piezo_position)
        # Divide the distance by the speed of sound and add it to the list
        times_of_flight.append(distance / SPEED_OF_SOUND)
    # Return the list of times of flight as an Autograd NumPy array
    return np.array(times_of_flight)


def timing_error(bubble_position, piezo_timings):
    """Calculate the mean squared error of the expected timings for a certain bubble positions versus those actually observed"""
    # Get the expected overall times of flight to the piezos for this bubble
    times_of_flight = expected_times_of_flight(bubble_position)
    # Subtract the minimum time of flight from all of them, so that the first signal is at time 0
    expected_timings = times_of_flight - np.min(times_of_flight)
    # Return the mean squared error between the actually observed piezo timings and the timings that would be expected for this bubble
    return np.linalg.norm(expected_timings - piezo_timings)


def localize_bubble(piezo_timings):
    """Calculate the position of a bubble, based on the timings of the signals to the piezos (of which the lowest value is expected to be 0), using error optimization"""
    # Convert the piezo timings to an Autograd NumPy array
    piezo_timings_numpy = np.array(piezo_timings)
    # Get the derivative of the timing error calculation function, used for optimization
    timing_error_derivative = grad(timing_error)
    # Optimize and return the position of the bubble, starting the search at (0, 0, 0)
    return minimize(
        fun=timing_error,
        x0=np.zeros(3),
        args=(piezo_timings_numpy,),
        method='BFGS',
        jac=timing_error_derivative
    ).x