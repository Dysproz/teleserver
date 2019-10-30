import calendar
import datetime

monthName = datetime.datetime.now().strftime("%B")
currentYear = datetime.datetime.now().year
currentMonth = datetime.datetime.now().month

def generate_month():
   calendar_ret = calendar.monthcalendar(currentYear, currentMonth)
   return calendar_ret

def print_title():
   return monthName  + " " + str(currentYear)

def change_next_month():
   if currentMonth == 12:
      currentMonth = 1
      currentYear = currentYear + 1
   else:
      currentMonth = currentMonth + 1
   monthName = datetime.datetime(currentYear,currentMonth,1)

def change_previous_month():
   if currentMonth == 1:
      currentMonth = 12
      currentYear = currentYear - 1
   else:
      currentMonth = currentMonth - 1
   monthName = datetime.datetime(currentYear,currentMonth,1)