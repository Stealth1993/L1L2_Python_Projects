#Iteration Method

def is_prime(number, divisor=2):
    if number <= 1:
        return False
    if divisor == number:
        return True
    if number % divisor == 0:
        return False
    return is_prime(number, divisor + 1)

num = int(input("Enter a number: "))

if is_prime(num):
    print(f"{num} is a prime number.")
else:
    print(f"{num} is not a prime number.")
	
	
#Square root method

def is_prime(number):
    if number <= 1:
        return False
    for i in range(2, int(number**0.5) + 1): #This loop checks for factors from 2 up to the square root of the number. If any divisor divides the number evenly, it returns False.
        if number % i == 0:
            return False
    return True
num = int(input("Enter a number: "))

if is_prime(num):
    print(f"{num} is a prime number.")
else:
    print(f"{num} is not a prime number.")