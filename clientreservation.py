from dataclasses import dataclass
import datetime
"""
Recruitment Task
This script holds a class containing client data
Author: Piotr Wołoszyk
"""


@dataclass
class ClientReservation():
    """
A dataclass to store the client's booking information
    Attributes:
        name : <string>
            first and last name of client
        start_date: <datetime>
            Reservation start date and time
        end_time: <datetime>
            Reservation end date and time
    """
    name: str
    start_date: datetime
    end_date: datetime
