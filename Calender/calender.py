def display_cal(year_ip, month_ip):
	import calendar
	print(calendar.month(year_ip, month_ip))


def fetch_year():

	while True:
		try:
			year_ip = int(input("Enter year: "))
			if year_ip < 0:
				raise ValueError("Year must be a +ve integer")
			return year_ip
		except ValueError:
			print("Invalid input. Please enter a valid year.")

def fetch_month():

	while True:
		try:
			month_ip = int(input("Enter month: "))
			if month_ip < 1 or month_ip > 12:
				raise ValueError("Value between 1 & 12")
			return month_ip
		except ValueError:
			print("Enter a valid month value.")

year_ip = fetch_year()
month_ip = fetch_month()

display_cal(year_ip, month_ip)