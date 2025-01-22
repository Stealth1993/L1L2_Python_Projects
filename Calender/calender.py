def display_cal(year_ip, month_ip):
    import calendar  # Importing the calendar module to work with dates
    print(calendar.month(year_ip, month_ip))  # Printing the calendar for the specified month and year

def fetch_year():
    while True:  # Continuously prompt for input until a valid year is provided
        try:
            year_ip = int(input("Enter year: "))  # Prompt user for year and convert it to an integer
            if year_ip < 0:
                raise ValueError("Year must be a +ve integer")  # Raise an error if the year is negative
            return year_ip  # Return the valid year input
        except ValueError:
            print("Invalid input. Please enter a valid year.")  # Prompt for re-entry if input is not valid

def fetch_month():
    while True:  # Continuously prompt for input until a valid month is provided
        try:
            month_ip = int(input("Enter month: "))  # Prompt user for month and convert it to an integer
            if month_ip < 1 or month_ip > 12:
                raise ValueError("Value between 1 & 12")  # Raise an error if the month is outside 1-12 range
            return month_ip  # Return the valid month input
        except ValueError:
            print("Enter a valid month value.")  # Prompt for re-entry if input is not valid

# Main Execution
year_ip = fetch_year()  # Fetch valid year from user
month_ip = fetch_month()  # Fetch valid month from user

display_cal(year_ip, month_ip)  # Display the calendar for the specified year and month
