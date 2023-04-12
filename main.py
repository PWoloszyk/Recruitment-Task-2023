"""
Recruitment Task
This script is the main program to handle tennis court bookings
Author: Piotr Wołoszyk
"""
import sys

from consts import WRONG_ANSWER_BANNER
from reservation import Reservation
from schedule import Schedule


def main():
    """Main function with REPL menu"""
    path_to_file = 'schedule'  # path to folder with csv and json file
    sch = Schedule()
    res = Reservation(sch)
    sch.load_csv(path_to_file)
    sch.load_json(path_to_file)
    while True:
        print('-'*30)
        print('Welcome to the Tennis Court Program!')
        print('-'*30)
        user_choice = input(
            'What do you want to do:\n'
            '1) Make a reservation\n'
            '2) Cancel a reservation\n'
            '3) Print schedule\n'
            '4) Save schedule to a file\n'
            '5) Exit\n'
            'Enter: 1, 2, 3, 4 or 5\n  $ ').strip()

        if user_choice == '1':
            res.make_reservation()
        elif user_choice == '2':
            res.cancel_reservation()
        elif user_choice == '3':
            res.print_schedule()
        elif user_choice == '4':
            res.save_schedule()
        elif user_choice == '5':
            sch.make_backup()
            sys.exit()
        else:
            print(WRONG_ANSWER_BANNER)


if __name__ == "__main__":
    main()
