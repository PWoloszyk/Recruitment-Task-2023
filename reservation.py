"""
Recruitment Task
This script allows you to create and delete reservations
Author: Piotr Wołoszyk
"""

from datetime import datetime, timedelta
from additionalexceptions import IsTooLate, StartOlderThanEnd
from schedule import Schedule
from consts import WRONG_ANSWER_BANNER


class Reservation():
    """
    The Reservation class includes methods to validate the date, name,
    make a reservation and cancel the reservation.
    Methods
        valid_date_time():
            Validate the format of date and time provided by the client
        valid_date():
            Validate the format of date provided by the client
        valid_name():
            Validate the name or last name provided by the client
        make_reservation():
            Make a new reservation
        cancel_reservation(booking_list):
            Cancel a reservation
        save_schedule()
            save schedule as a csv or json file
        print_schedule()
            print the schedule to the terminal
    """
    def __init__(self, schedule):
        self.sch = schedule

    def valid_date_time(self, date):
        """
        Validate the format of date and time provided by the client
        Valid date should be in {DD.MM.YYYY HH:MM} format and
        be later than in an hour

        Return <datetime>
        """
        date_format = '%d.%m.%Y %H:%M'  # valid date format
        # date an hour later
        time_now = datetime.now() + timedelta(minutes=60)
        try:
            date = datetime.strptime(date, date_format)
            date + timedelta(minutes=90)
            if time_now >= date:
                raise IsTooLate
            return date
        except ValueError:
            print(
                '! Wrong format. should use date format {DD.MM.YYYY HH:MM} !')
            return None
        except IsTooLate:
            print("! It's already to late to book this!")
            return None
        except OverflowError:
            print("! This date is too far  from now!")
            return None

    def valid_date(self):
        """
        Validate the format of date provided by the client
        Valid date should be in {DD.MM.YYYY} format

        Return <datetime>
        """
        date_format = '%d.%m.%Y'  # Valid date format
        try:
            start_date = input(
                'Enter the start date as {DD.MM.YYYY}\n  $ ').strip()
            start_date = datetime.strptime(start_date, date_format).date()
            end_date = input(
                'Enter the end date as {DD.MM.YYYY} \n  $ ').strip()
            end_date = datetime.strptime(end_date, date_format).date()
            if start_date > end_date:
                raise StartOlderThanEnd
        except ValueError:
            print(
                '! Wrong format. should use date format {DD.MM.YYYY}!')
            return None, None
        except OverflowError:
            print("! Date is too far from now!")
            return None, None
        except StartOlderThanEnd:
            print('! The start date is older than the end date!')
            return None, None
        return start_date, end_date

    def valid_name(self, fullname):
        """
        Validate the name or last name provided by the client
        valid names should be alphabetical and longer than 2 character

        Return <string>
        """

        if len(fullname) <= 1:
            print('! Name is to short !')
            return
        if fullname.find(' ') == -1:
            print('! You must enter your first name and surname !')
            return
        if all(
                name.isalpha()
                or name.isspace()
                or name == '-'
                for name in fullname):
            return fullname.strip()
        print('! Name is wrong !')
        return

    def make_reservation(self):
        """
        Make a new reservation
        It takes the client's name, last name and date,
        checks these values and creates new reservations
        Args:
           <list> booking_list - list of client_reservation object
        """

        fullname = self.valid_name(
            input('Enter your fullname:\n  $ ').strip())  # Get client's name
        if fullname is None:
            return
        print('The court is open 24/7, but please note that:\n'
              '1) you can only have 2 bookings per week\n'
              '2) Reservations can be made at least one hour in advance')
        # booking start date
        start_date = self.valid_date_time(
            input('Enter date as {DD.MM.YYYY HH:MM}:\n  $ ').strip())  # Get client's desired start date
        if start_date is None:
            return
        # Check if the desired start date is available
        new_date, hour = self.sch.date_is_free(start_date)

        if new_date is None:
            return

        # If the desired start date is not available, suggest a new date
        answer_new_date = ''
        date_format = '%d.%m.%Y %H:%M'  # valid date format
        if new_date != start_date:
            answer_new_date = input('The time you chose is unavailable,'
                                    'would you like to make a reservation'
                                    f'for {new_date.strftime(date_format)}'
                                    'instead? (yes/no)\n  $ ').strip()
        if answer_new_date.lower() == 'yes':
            start_date = new_date
        elif answer_new_date.lower() == 'no':
            print('The court is open 24/7, but please note that:\n'
                  '1) you can only have 2 bookings per week\n'
                  '2) Reservations can be made at least one hour in advance')
            self.valid_date_time()
        elif answer_new_date != '':
            print(WRONG_ANSWER_BANNER)
            return

        # Check if a client has too many reservations for this week
        if self.sch.too_many_reservation(fullname,
                                         start_date):
            print('! You have exceeded your booking limit for this week!')
            return

        # Determine available hours for the reservation
        which_number = {
            0: '1)30 minutes',
            1: '1)30 minutes\n2)60 minutes',
            2: '1)30 minutes\n2)60 minutes\n3)90 minutes'
        }

        for key, value in which_number.items():
            if hour == key:
                available_hours = value

        # Get the duration of the reservation
        answer = input(
            'How long would you like to book court?\n'
            f'{available_hours}\n  $ ').strip()

        if answer == '1':
            end_date = start_date + timedelta(minutes=30)
        elif answer == '2' and hour != 0:
            end_date = start_date + timedelta(minutes=60)
        elif answer == '3' and hour == 2:
            end_date = start_date + timedelta(minutes=90)
        else:
            print(WRONG_ANSWER_BANNER)
            return

        # Add the reservation to the schedule
        self.sch.add_reservation(fullname, start_date, end_date)
        return

    def cancel_reservation(self):
        """
        Cancel a reservation
        It takes the client's name, last name and date,
        checks these values and cancel reservations

        Args:
            <list> booking_list - list of client_reservation object
        """
        print('Please note that reservations can be'
              ' canceled up to one hour in advance')
        name = self.valid_name(
            input('Enter your fullname:\n  $ ').strip()
        )  # Client's name
        if name is None:
            return
        date = self.valid_date_time(
            input('Enter date as {DD.MM.YYYY HH:MM}:\n  $ ').strip())  # Date of reservation to cancel
        if date is None:
            return

        # Check if a reservation exists
        index = self.sch.reservation_exists(
            name, date)
        if index == -1:
            print('! There is no reservation for You on this specified date!')
            return
        # current system time
        time_now = datetime.now() + timedelta(minutes=60)
        if time_now >= date:
            print('! Is too late to cancel!')
            return
        answer = input('Are you sure? (yes/no)\n  $ ').strip()
        if answer.lower() == 'yes':
            self.sch.delete_reservation(index)
            return
        if answer.lower() == 'no':
            return
        print(WRONG_ANSWER_BANNER)
        return

    def save_schedule(self):
        """
        Ask client about file format and file name
        """
        if self.sch.is_empty():
            print('! Schedule is empty!')
            return
        start_date, end_date = self.valid_date()
        if start_date is None:
            return
        filename = input('Enter a file name:\n  $ ').strip()
        file_extension = input('Save file as:\n1)csv\n2)json?\n  $ ').strip()
        if file_extension == '1':
            self.sch.save_csv(start_date, end_date,
                              filename.strip())
            return
        if file_extension == '2':
            self.sch.save_json(start_date, end_date,
                               filename.strip())
            return
        print(WRONG_ANSWER_BANNER)
        return

    def print_schedule(self):
        """
        Ask client for a start and end date
        """
        if self.sch.is_empty():
            print('! Schedule is empty!')
            return
        start_date, end_date = self.valid_date()
        if start_date is None:
            return
        self.sch.print_schedule_output(start_date, end_date)
        try:
            input('Press Enter to continue')
        except ValueError:
            return
        return

        