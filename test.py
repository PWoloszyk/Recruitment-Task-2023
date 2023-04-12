from datetime import datetime

from reservation import Reservation
from schedule import Schedule
from clientreservation import ClientReservation
from unittest.mock import patch


class TestSchedule():
    """

    Schedule.Schedule method tests
    """
    date_format = '%d.%m.%Y %H:%M'
    sch = Schedule()
    booking_list = []

    def test_date_is_free(self):
        """
        Test the date_is_free method
        """

        # New reservation
        s_date = datetime.strptime('25.04.2023 15:00', self.date_format)
        e_date = datetime.strptime('25.04.2023 16:00', self.date_format)
        self.sch.booking_list.append(ClientReservation(
            'Piotr W',
            s_date,
            e_date
        ))

        # No reservations for this date and for the next 1.5 hours
        date = datetime.strptime('25.04.2023 11:11', self.date_format)
        # The method return:
        #   input date
        #   2 - We can make reservations for 0.5h ,1h or 1.5h
        assert self.sch.date_is_free(date) == (date, 2)

        # No reservations for this date and for the next 1 hours
        date = datetime.strptime('25.04.2023 14:00', self.date_format)
        # The method return:
        #   input date
        #   1 - because someone has a reservation in an hour
        assert self.sch.date_is_free(date) == (date, 1)

        # There is a reservation for this date
        date = datetime.strptime('25.04.2023 15:15', self.date_format)
        # The method return:
        #   end_date from booking_list (25.04.2023 16:00)
        #   2 - because there are no others dates after that date
        assert self.sch.date_is_free(date) == (
            datetime.strptime('25.04.2023 16:00', self.date_format), 2)

    def test_reservation_exists(self):
        """
        Test reservation_exists method
        """

        # There is a reservation for this name and this day
        name = 'Piotr W'
        date = datetime.strptime('25.04.2023 15:00', self.date_format)
        # The method return:
        #   1 - reservation index in the booking_list
        assert self.sch.reservation_exists(name, date) == 0

        # There are no reservations for this name or for this day
        name = 'Jan kowalski'
        date = datetime.strptime('25.04.2023 17:00', self.date_format)
        # The method return:
        #   -1 - there is no such index in the booking_list
        assert self.sch.reservation_exists(name, date) == -1

    def test_too_many_reservation(self):
        """
        Test too_many_reservation method
        """
        # 'Piotr W' currently has one booking day 25.04.2023
        date = datetime.strptime('25.04.2023 13:00', self.date_format)
        # The method return:
        #   False - He still can make a reservation
        assert self.sch.too_many_reservation(
            'Piotr W', date) is False

        # We are adding one more booking for 'Piotr W' for 25.04.2023
        s_date = datetime.strptime('25.04.2023 17:00', self.date_format)
        e_date = datetime.strptime('25.04.2023 18:00', self.date_format)
        self.sch.booking_list.append(ClientReservation(
            'Piotr W',
            s_date,
            e_date
        ))
        # The method return:
        #   True - he has reached his booking limit for this week
        date = datetime.strptime('25.04.2023 20:00', self.date_format)
        assert self.sch.too_many_reservation(
            'Piotr W', date) is True


class TestReservation():
    """
    reservation.Reservation method tests
    """

    date_format = '%d.%m.%Y %H:%M'
    sch = Schedule()
    res = Reservation(sch)

    def test_print_schedule(self, capsys):
        """
        Test print_schedule method
        """
        # add second reservation
        s_date = datetime.strptime('25.04.2023 17:00', self.date_format)
        e_date = datetime.strptime('25.04.2023 18:00', self.date_format)
        self.sch.booking_list.append(ClientReservation(
            'Piotr W',
            s_date,
            e_date))
        # simulating input
        user_input = ['25.04.2023', '25.04.2023', '']
        with patch('builtins.input', side_effect=user_input):
            self.res.print_schedule()
        # reading output
        captured = capsys.readouterr()
        # expected answer
        correct_answer = ('Tuesday\n'
                          '\t*Piotr W 25.04.2023 15:00 - 25.04.2023 16:00\n'
                          '\t*Piotr W 25.04.2023 17:00 - 25.04.2023 18:00\n'
                          '\t*Piotr W 25.04.2023 17:00 - 25.04.2023 18:00\n')

        assert captured.out == correct_answer

    def test_valid_date_time(self):
        """
        Test the valid_date method
        """

        # The date is correct
        input_date = '25.04.2023 15:00'
        # The method return:
        #   input_date in datetime format
        assert self.res.valid_date_time(input_date) == datetime.strptime(
            '25.04.2023 15:00', self.date_format)

        # the date is incorrect (no time)
        input_date = '25.03.2023'
        # the method return:
        #   None
        assert self.res.valid_date_time(input_date) is None

    def test_valid_name(self):

        # Name is correct
        input_name = 'Piotr W'
        # The method return
        #   string same as input
        assert self.res.valid_name(input_name) == 'Piotr W'

        # Name is incorrect (no surname)
        input_name = 'Piotr'
        # the method return:
        #   None
        assert self.res.valid_name(input_name) is None
