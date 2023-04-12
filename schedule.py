"""
Recruitment Task
This script allows you to load reservations from a csv or json file,
saving the reservation to this file
printing the reservation in the terminal
operations on the reservation list

Author: Piotr Wołoszyk
"""

import csv
import json
from datetime import datetime, timedelta
from pathlib import Path

from clientreservation import ClientReservation
from consts import WRONG_ANSWER_BANNER


class Schedule():
    """
    The schedule class includes methods to load data from csv and json files,
    print and save reservations for the dates selected by the client
    and a method to prevent duplicate bookings
    Methods:
        new_booking():
            Check if the reservation already exists
        load_json():
            Load data from json files.
        load_csv():
            Load data from csv files.
        print_schedule_output():
            Print the schedule
        save_schedule():
            Save the schedule to a file in the path provided by the client
        save_csv():
            Save the schedule as a csv file
        save_csv():
            Save the schedule as a json file
        too_many_reservation():
            Check if a client has exceeded the booking limit for this week
        reservation_exists():
            Check if a reservation exists
        is_empty():
            Checks if the reservation list is empty
        add_reservation():
            adds reservations to the list
        delete_reservation():
            Removes reservations from the list
        date_is_free():
            Check if a provided date is free and how long will be
    """

    booking_list = []  # list of all bookings

    def is_empty(self):
        """
        Checks if the reservation list is empty
        return: <bool>
            True if is empty
            False otherwise
        """
        if len(self.booking_list) == 0:
            return True
        return False

    def add_reservation(self, fullname, start_date, end_date):
        """
        adds reservations to the list
        Args:
            <string> fullname - client's name
            <datetime> start_date - booking start date
            <datetime> end_date - booking end date
        """
        self.booking_list.append(ClientReservation(
            fullname,
            start_date,
            end_date))
        print('Booking successful!')
        return

    def delete_reservation(self, index):
        """
        Removes reservations from the list
        Args:
            <int> index - reservation index to be deleted
        """
        del self.booking_list[index]
        print('Reservations have been cancelled!')
        return

    def too_many_reservation(self, name, date):
        """
        Check if a client has exceeded the booking limit for this week

        Args:
            <sting> name - client's name
            <datetime> date - the date the client wants to book
        Return <bool>:
            True when the client has used up the booking limit
            False when client still can book
        """

        booking = []  # list of checked client's reservations
        # day one week later from provided date
        week_start_date = date - timedelta(days=date.weekday())
        try:
            week_end_date = week_start_date + timedelta(days=6)
        except OverflowError:
            week_end_date = date
        if date > week_end_date:
            return False
        for reservation in self.booking_list:
            if reservation.name == name:
                booking.append(reservation.start_date)
        counter = 0
        for book in booking:
            if week_start_date <= book < week_end_date:
                counter += 1
        if counter >= 2:
            return True
        return False

    def reservation_exists(self, name, date):
        """
        Check if a reservation exists

        Args:
            <string> name - client's name
            <datetime> date - the date of the booking to cancel
        Return <int>:
            if the reservation exists returns the index of the reservation,
            if not returns -1
        """

        index = 0  # client's booking index
        # iterating through the reservations and
        # check if one provided by the client exists
        for reservation in self.booking_list:
            date_on_list = reservation.start_date

            if reservation.name == name\
                    and date_on_list == date:
                return index
            index += 1
        return -1

    def date_is_free(self, date):
        """
        Check if a provided date is free and how long will be

        Args:
            <datetime> date - date provided by the client

        Return:
            1)<datetime>
                date - if provided date is free date = provided date,
                if not date = first free date
            2)<int>
                2 if court will be available for 1,5h
                1 if court will be available for 1h
                0 if court will be available for 0,5h
        """

        self.booking_list.sort(key=lambda x: x.start_date)
        # hold date 0,5h later then provided
        sixty_minutes = date + timedelta(minutes=30)
        # hold date 1h later then provided
        ninety_minutes = date + timedelta(minutes=60)

        # iterating over reservations
        # and check in how long court will be available
        for reservation in self.booking_list:
            start_date = reservation.start_date
            end_date = reservation.end_date
            try:
                end_date + timedelta(minutes=90)
            except OverflowError:
                print('! This date is too far  from now!')
                return None, None
            if start_date <= date < end_date:
                date = end_date
                sixty_minutes = date + timedelta(minutes=30)
                ninety_minutes = date + timedelta(minutes=60)
            if start_date <= sixty_minutes < end_date:
                sixty_minutes = end_date
            if start_date <= ninety_minutes < end_date:
                ninety_minutes = end_date
        if date + timedelta(minutes=30) == sixty_minutes and\
                date + timedelta(minutes=60) == ninety_minutes:
            return date, 2
        if date + timedelta(minutes=30) == sixty_minutes:
            return date, 1
        return date, 0

    def new_booking(self, name, start_date, end_date):
        """
        Check if the reservation already exists
        Args:
            <string> name - Client's name
            <datetime> start_date - Reservation start date
            <datetime> end_date - Reservation end date

        Return <bool>:
            False reservation already exists or True when is not
        """
        # iterate through the reservations and see if it already exists
        for reservation in self.booking_list:
            if (reservation.name == name
                    and reservation.start_date == start_date
                    and reservation.end_date == end_date):
                return False
        return True

    def load_csv(self, path_to_file):
        """
        Load data from csv files.
        Args:
            <string> path_to_file - hold path to folder with csv file
        """

        date_format = '%d.%m.%Y %H:%M'  # valid date format
        # load from csv files
        all_csv_paths = Path(path_to_file).glob("*.csv")
        for csv_path in all_csv_paths:
            print(f"Found: {csv_path}")
            with open(csv_path, 'r', encoding='UTF-8') as csv_file:
                csv_line = csv.reader(csv_file)
                _ = next(csv_line)
                for row in csv_line:
                    name = row[0].strip()
                    try:
                        start_date = row[1].strip()
                        start_date = datetime.strptime(start_date, date_format)
                        end_date = row[2].strip()
                        end_date = datetime.strptime(end_date, date_format)
                    except ValueError:
                        print(f'{csv_path} upload failed')
                        return
                    # saving reservations on the list
                    if self.new_booking(name,
                                        start_date,
                                        end_date):
                        self.booking_list.append(ClientReservation(
                            name, start_date, end_date))
        return

    def load_json(self, path_to_file):
        """
        Load data from csv or json files.
        Args:
            <string> path_to _file - hold path to folder with json file
        """

        date_format = '%d.%m.%Y %H:%M'  # valid date format
        # load from json files
        all_json_paths = Path(path_to_file).glob("*.json")
        for json_path in all_json_paths:
            print(f"Found: {json_path}")
            with open(json_path, 'r', encoding='UTF-8') as json_file:
                data = json.load(json_file)
            for key, values in data.items():
                for row in values:
                    name = row['name'].strip()
                    if len(key) == 10:
                        try:
                            start_date = f'{key} {row["start_time"]}'
                            start_date = datetime.strptime(start_date, date_format)
                            end_date = f'{key} {row["end_time"]}'
                            end_date = datetime.strptime(end_date, date_format)
                        except ValueError:
                            print(f'{json_path} upload failed')
                            return
                    else:
                        try:
                            start_date = f'{key}.2023 {row["start_time"]}'
                            start_date = datetime.strptime(start_date, date_format)
                            end_date = f'{key}.2023 {row["end_time"]}'
                            end_date = datetime.strptime(end_date, date_format)
                        except ValueError:
                            print(f'{json_path} upload failed')
                            return

                    # saving reservations on the list
                    if self.new_booking(name,
                                        start_date,
                                        end_date):

                        self.booking_list.append(ClientReservation(
                            name, start_date, end_date))

    def print_schedule_output(self, start_date, end_date):
        """
        Print the schedule
        Args:
            <datetime> start_date - start date to print
            <datetime> end_date - end date to print
        """

        # the key of the dictionary is data, the value is the client's data
        booking_dictionary = {}
        time_now = datetime.now()  # current system time
        # sort the list to find last day
        self.booking_list.sort(key=lambda x: x.end_date, reverse=True)
        last_date_on_list = self.booking_list[0].end_date.date()

        # sort the list by start date
        self.booking_list.sort(key=lambda x: x.start_date)
        first_date_on_list = self.booking_list[0].start_date.date()
        # first date to check
        if start_date < first_date_on_list:
            print(f'The first date on the schedule is '
                  f"{first_date_on_list.strftime('%d.%m.%Y')}")
        if end_date > last_date_on_list:
            print(f'The last date on the schedule is '
                  f"{last_date_on_list.strftime('%d.%m.%Y')}")
        one_day_reservations = []  # all bookings in one day
        # iterating over reservations
        for reservation in self.booking_list:
            # date of the current reservation
            date = (reservation.start_date).date()
            # check if no bookings have been found for the day
            for key, value in booking_dictionary.items():
                if key == date:
                    one_day_reservations = (value)
            # search for new one
            if start_date <= date <= end_date:
                one_day_reservations.append(
                    str(reservation.name + ' '
                        + (reservation.start_date).strftime('%d.%m.%Y %H:%M')
                        + ' - '
                        + (reservation.end_date).strftime('%d.%m.%Y %H:%M')))
            # save all reservations from one day to the dictionary
            if len(one_day_reservations) != 0:
                booking_dictionary.setdefault(
                    date, one_day_reservations)
                one_day_reservations = []
        if len(booking_dictionary) == 0:
            print('no reservations on selected dates')
        for key, value in booking_dictionary.items():
            if time_now.date() == key:
                print('Today')
            elif time_now.date() + timedelta(days=1) == key:
                print('Tomorrow')
            else:
                day_of_week = key.strftime('%A')
                print(day_of_week)
            for reservation in value:
                print(f'\t*{reservation}')
        return

    def save_csv(self, start_date, end_date, filename):
        """
        Save the schedule to a csv file with a name provided by the client
        Args:
            <datetime> start_date - from that date
            <datetime> end_date - by this date

        """

        date_format = '%d.%m.%Y'  # valid date format
        # sort list by date
        first_date_on_list, last_date_on_list = self.list_sort()
        # first date to check
        if start_date < first_date_on_list:
            print(f'First date on the list is '
                  f' {first_date_on_list.strftime(date_format)}')
        if end_date > last_date_on_list:
            print(f'Last date on the list is '
                  f'{last_date_on_list.strftime(date_format)}')
        # Creates a file and writes a list to it
        with open(f'{filename}.csv', 'w', newline='', encoding='UTF-8')\
                as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Name', ' start_time', ' end_time'])
            # iterating over reservations
            for reservation in self.booking_list:
                # date of the current reservation
                date = reservation.start_date.date()
                # checking if there are reservations for that day
                if start_date <= date <= end_date:
                    name = reservation.name
                    s_date = ' ' + (reservation.start_date).strftime(
                        '%d.%m.%Y %H:%M')
                    e_date = ' ' + \
                        (reservation.end_date).strftime('%d.%m.%Y %H:%M')
                    writer.writerow([name, s_date, e_date])

    def list_sort(self):
        """
        sort list to find last date on the list
        sort list to find first date on the list
        Return:
            <datetime> first_date_on_list - from that date
            <datetime> last_date_on_list - by this date

        """
        # sort the list to find last day
        self.booking_list.sort(key=lambda x: x.end_date, reverse=True)
        last_date_on_list = self.booking_list[0].end_date.date()

        # sort the list by start date
        self.booking_list.sort(key=lambda x: x.start_date)
        first_date_on_list = self.booking_list[0].start_date.date()
        return first_date_on_list, last_date_on_list

    def save_json(self, start_date, end_date, filename):
        """
        Save the schedule to a json file with a name provided by the client
        Args:
            <datetime> start_date - from that date
            <datetime> end_date - by this date
        """

        date_format = '%d.%m.%Y'  # valid date format
        booking_dictionary = {}  # dictionary of client_reservation object
        one_client = {}  # client data dictionary
        one_day_reservations = []  # one day booking list
        # sort list by date
        first_date_on_list, last_date_on_list = self.list_sort()
        if start_date < first_date_on_list:
            print('First date on the list is '
                  f'{first_date_on_list.strftime(date_format)}')
        if end_date > last_date_on_list:
            print(f'Last date on the list is '
                  f'{last_date_on_list.strftime(date_format)}')

        # iterating over reservations
        for reservation in self.booking_list:
            # date of the current reservation
            date = reservation.start_date.date()
            # check if no bookings have been found for the day
            for key, value in booking_dictionary.items():
                if datetime.strptime(key, date_format).date() == date:
                    one_day_reservations = value
            # search for new one
            if start_date <= date <= end_date:
                one_client['name'] = str(reservation.name)
                _, s_time = ((reservation.start_date).strftime(
                    '%d.%m.%Y %H:%M')).split(' ')
                one_client['start_time'] = s_time
                _, e_time = ((reservation.end_date).strftime(
                    '%d.%m.%Y %H:%M')).split(' ')
                one_client['end_time'] = e_time
                one_day_reservations.append(one_client)
                one_client = {}
            if len(one_day_reservations) != 0:
                booking_dictionary[
                    date.strftime(date_format)] = one_day_reservations
                one_day_reservations = []

        # Creates a file and writes a dictionary to it
        with open(f'{filename}.json', 'w', encoding='UTF-8')\
                as json_file:
            json.dump(booking_dictionary,
                      json_file,
                      ensure_ascii=False,
                      indent=4)

    def make_backup(self):
        """
        saves the schedule to a csv file when closing the program
        """
        # sort list by date
        start_date, end_date = self.list_sort()

        date_format = '%d.%m.%Y'  # valid date format
        # sort list by date
        first_date_on_list, last_date_on_list = self.list_sort()
        # first date to check
        if start_date < first_date_on_list:
            print(f'First date on the list is '
                  f' {first_date_on_list.strftime(date_format)}')
        if end_date > last_date_on_list:
            print(f'Last date on the list is '
                  f'{last_date_on_list.strftime(date_format)}')
        # Creates a file and writes a list to it
        with open(f'schedule/last_session.csv', 'w', newline='', encoding='UTF-8')\
                as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Name', ' start_time', ' end_time'])
            # iterating over reservations
            for reservation in self.booking_list:
                # date of the current reservation
                date = reservation.start_date.date()
                # checking if there are reservations for that day
                if start_date <= date <= end_date:
                    name = reservation.name
                    s_date = ' ' + (reservation.start_date).strftime(
                        '%d.%m.%Y %H:%M')
                    e_date = ' ' + \
                        (reservation.end_date).strftime('%d.%m.%Y %H:%M')
                    writer.writerow([name, s_date, e_date])
