import calendar
import datetime


class CalendarTime():

    def __init__(self, monthName, currentYear, currentMonth):
        self.monthname = monthName
        self.year = currentYear
        self.month = currentMonth


def generate_month(CalTimeObject):
    """
    Generate month's calendar as a matrix

    :param CalTimeObject: Object with month, year, name of the month
    :return: Matrix 6x7 with a days in a month
    :rtype: list
    """
    calendar_ret = calendar.monthcalendar(CalTimeObject.year, CalTimeObject.month)
    return calendar_ret


def print_title(CalTimeObject):
    """
    Concatenate current month and year

    :param CalTimeObject: Object with month, year, name of the month
    :return: Month name and a year
    :rtype: string
    """
    return str(CalTimeObject.monthname) + " " + str(CalTimeObject.year)


def change_next_month(CalTimeObject):
    """
    Change a current month and year (if necessary) to a next one

    :param CalTimeObject: Object with month, year, name of the month
    """
    if CalTimeObject.month == 12:
        CalTimeObject.month = 1
        CalTimeObject.year = CalTimeObject.year + 1
    else:
        CalTimeObject.month = CalTimeObject.month + 1
    CalTimeObject.monthname = datetime.datetime(CalTimeObject.year, CalTimeObject.month, 1).strftime("%B")


def change_previous_month(CalTimeObject):
    """
    Change a current month and a year (if necessary) to a previous one

    :param CalTimeObject: Object with month, year, name of the month
    """
    if CalTimeObject.month == 1:
        CalTimeObject.month = 12
        CalTimeObject.year = CalTimeObject.year - 1
    else:
        CalTimeObject.month = CalTimeObject.month - 1
    CalTimeObject.monthname = datetime.datetime(CalTimeObject.year, CalTimeObject.month, 1).strftime("%B")
