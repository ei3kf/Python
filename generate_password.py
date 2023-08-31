#!/usr/bin/env python3

"""
generate_password.py
  - create alphanumeric including special characters password.
"""

import random
import string
import argparse


def generate_password(length):
    """
    generate a random alphanumeric with special
    characters string of a given length.
    """
    password = ''.join([random.SystemRandom().choice(
                       string.ascii_letters
                       + string.digits
                       + '!@#$%^&(')
                       for n in range(length)])
    return password


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--length",
        help="Length of password to create.",
        type=int,
        default=16
        )

    args = parser.parse_args()
    password = generate_password(args.length)
    print("{}").format(password)
