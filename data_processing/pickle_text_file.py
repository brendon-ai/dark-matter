#!/usr/bin/env python3
"""A script for converting data serialized as a text file to the Pickle format that is loaded when running training or analysis"""
# Created by Brendon Matusch, July 2018

import os

from functools import reduce

from data_processing.event_data_set import EVENT_FILE_PATH

# A dictionary corresponding the last letter of a format string to the type of that element
TYPES_BY_FORMAT = {
    'd': int,
    'e': float,
    'f': float,
    's': str
}

# Open the text file and read it line by line
with open(os.path.expanduser('~/merged_all.txt')) as text_file:
    # Read and ignore the first line, which contains useless description
    text_file.readline()
    # Read the second line, strip it, and split it on whitespace; it includes the names and dimensions of attributes in the file
    attributes = text_file.readline().strip().split()
    # Iterate over the attributes, adding to lists of names and corresponding numbers of sub-elements
    attribute_names = []
    attribute_elements = []
    for attribute in attributes:
        # If there are no brackets containing numbers of elements, add the name and set the number of elements to 1
        if '(' not in attribute:
            attribute_names.append(attribute)
            attribute_elements.append(1)
        # Otherwise, we need to handle a multi-element attribute
        else:
            # Split the attribute description by the open bracket and extract the name, which is before the brackets
            attribute_split = attribute.split('(')
            attribute_names.append(attribute_split[0])
            # After the open bracket is a comma-separated list of numbers with a close bracket at the end; separate the dimension numbers
            dimensions = [int(number_string.strip()) for number_string in attribute_split[1][:-1].split(',')]
            # Multiply each of the dimensions together to get the total number of elements in this attribute, and add it to the list
            elements = reduce(lambda first, second: first * second, dimensions)
            attribute_elements.append(elements)
    # Read and split the next line, which contains format strings for every element in the lines ahead
    format_strings = text_file.readline().strip().split()
    # Take only the last letter of each format string, which denotes the type, and get the types corresponding to these from the dictionary
    attribute_types = [TYPES_BY_FORMAT[format_string[-1]] for format_string in format_strings]
    print(attribute_types)
