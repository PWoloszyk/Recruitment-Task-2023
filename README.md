# Recruitment Task
## Overview
This is the task in the recruitment process for the position of Intern Python Developer. It is a REPL program allows user to:  
&emsp;1.Make a reservation  
&emsp;2.Cancel a reservation  
&emsp;3.Print schedule  
&emsp;4.Save schedule to a file  
&emsp;5.Exit 

## Requirements
**Python 3.10 or above** 

I have imported several libraries from standard library into my program, such as: sys, csv, json, datetime, pathlib or dataclasses.

I also imported PyTest library for unit tests.

**Pytest** is a popular third-party testing framework for Python. It provides a simple and flexible way to write and run tests for your Python code.

Some of the key features of pytest include:

Test discovery: pytest can automatically discover and run tests in your project without requiring you to manually specify which tests to run.

Fixtures: pytest provides a powerful fixture system for setting up and tearing down test environments, making it easy to write tests that are independent and repeatable.

Parametrized testing: pytest allows you to write tests that are parameterized with different inputs, making it easy to test your code with a variety of scenarios and edge cases.

To use pytest, you first need to install it. You can use the command below.
```bash
pip install -r requirements.txt
``` 
## Instruction
After starting, the program loads the schedule from csv and json files from the folder 'schedule'. The program has protection against duplication of records. To run, use the following commands

```bash
python3 main.py
``` 
## How it work
### 1. Make a reservation
Program ask about:  
&emsp;1.Fullname  
&emsp;2.Booking date 

Program valid both value. Proper fullname shuld have more than 1 character, must be alphabetic and hava at least two parts separated by a space (name and surname). Valid date must be in format {DD.MM.YYYY HH:MM}. Moreover, no more than two bookings can be made in one week, and bookings must be made at least one hour in advance. If you try, the program does not ask for an answer again, but returns to the main menu. What's more, you can book a court for 0.5h, 1h or 1.5h as long as it's not busy.

### 2. Cancel a reservation  
Program ask about:  
&emsp;1.Fullname  
&emsp;2.booking date 

As above program valid both value. You can cancel your reservation up to an hour before and only if it exists. Similar to booking, if you try, the program doesn't ask for an answer again, but returns to the main menu.

### 3. Print schedule
Program ask about:  
&emsp;1.Start date  
&emsp;2.End date

Valid format is {DD.MM.YYYY}. The dates indicate the range of interest. If you don't make mistake, you'll see a schedule with days of the week and reservations for that day.

### 4. Save schedule to a file
Program ask about:  
&emsp;1.Start date  
&emsp;2.End date  
&emsp;3.file name  
&emsp;4.file format

Valid format is {DD.MM.YYYY}. As above the dates indicate the range of interest. File name could be path to folder. You can choose between cvs or json file format.

### 5. Exit
Creates a "last_session" file in schedule subfolder that saves all schedule changes and ends the program.

## Running Tests

I have prepared 6 tests checking a few minor methods in the program. To run, use the following command

```bash
  pytest test.py
```


## Author

Piotr Wołoszyk

