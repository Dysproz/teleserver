import calendar
import datetime

monthName = datetime.datetime.now().strftime("%B")
currentYear = datetime.datetime.now().year
currentMonth = datetime.datetime.now().month


def generate_month():
   """
   Generate month's calendar as a matrix

   :return: Matrix 6x7 with a days in a month
   :rtype: list
   """
   global currentYear
   global currentMonth
   calendar_ret = calendar.monthcalendar(currentYear, currentMonth)
   return calendar_ret

def print_title():
   """
   Concatenate current month and year

   :return: Month name and a year
   :rtype: string
   """
   return str(monthName)  + " " + str(currentYear)

def change_next_month():
   """
   Change a current month and year (if necessary) to a next one
   """
   global currentMonth
   global currentYear
   global monthName
   if currentMonth == 12:
      currentMonth = 1
      currentYear = currentYear + 1
   else:
      currentMonth = currentMonth + 1
   monthName = datetime.datetime(currentYear,currentMonth,1).strftime("%B")

def change_previous_month():
   """
   Change a current month and a year (if necessary) to a previous one
   """
   global currentMonth
   global currentYear 
   global monthName
   if currentMonth == 1:
      currentMonth = 12
      currentYear = currentYear - 1
   else:
      currentMonth = currentMonth - 1
   monthName = datetime.datetime(currentYear,currentMonth,1).strftime("%B")
