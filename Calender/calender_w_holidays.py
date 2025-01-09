import calendar
import holidays

def display_cal(year_ip, month_ip):
    print(calendar.month(year_ip, month_ip))

def fetch_year():
    while True:
        try:
            year_ip = int(input("Enter year: "))
            if year_ip < 0:
                raise ValueError("Year must be a positive integer")
            return year_ip
        except ValueError:
            print("Invalid input. Please enter a valid year.")

def fetch_month():
    while True:
        try:
            month_ip = int(input("Enter month: "))
            if month_ip < 1 or month_ip > 12:
                raise ValueError("Value between 1 and 12")
            return month_ip
        except ValueError:
            print("Enter a valid month value.")

def fetch_holidays(year_ip, month_ip):
    india_holidays = holidays.India(years=year_ip)
    month_holidays = {}
    for date, name in sorted(india_holidays.items()):
        if date.month == month_ip:
            month_holidays[date.day] = name
    return month_holidays

year_ip = fetch_year()
month_ip = fetch_month()

display_cal(year_ip, month_ip)
holidays = fetch_holidays(year_ip, month_ip)
if holidays:
    for day, holiday in holidays.items():
        print(f"{holiday}: {calendar.month_name[month_ip]} {day}, {year_ip}")
else:
    print(f"No holidays found for {calendar.month_name[month_ip]} {year_ip}")
