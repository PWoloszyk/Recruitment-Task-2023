"""
Recruitment Task
This file holds all additional exceptions
Author: Piotr Wołoszyk
"""


class IsTooLate(Exception):
    """
    Exception raised when a client tries to reserve within an hour from now
    """


class StartOlderThanEnd(Exception):
    """
    Exception raised when the start date is older than the end date
    """
