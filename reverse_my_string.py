#!/usr/bin/python

"""
Reverse a given string.
"""

import argparse


class ReverseString(object):
    """
    Class to reverse the contents of a given string.
    """

    def __init__(self, input_string):
        self.input_string = input_string
        self.output_string = ""


    def reversed(self):
    	"""
    	reversed method - takes length of given string, with a for loop
    	create a new string with the characters in reverse.
    	"""
    	self.input_length = len(self.input_string) - 1
    	for count in range(self.input_length, -1, -1):
			self.output_string = self.output_string + self.input_string[count]

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        help="String to reverse.",
        required=True,
        type=str)

    args = parser.parse_args()

if args.input:
    my_string = ReverseString(args.input)
    my_string.reversed()
    print("Forward : {}  Reverse : {}").format(my_string.input_string,my_string.output_string)

