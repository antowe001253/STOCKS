import sys, os
import requests
import calendar
import datetime

def getdays(month,year):
	num_days = calendar.monthrange(year, month)[1]
	days = [datetime.date(year, month, day) for day in range(1, num_days+1)]
	return days

days=getdays(1,2018)


for each_day in days:
        print(each_day)

print("==================[ D O N E ]==================")
k=input()
