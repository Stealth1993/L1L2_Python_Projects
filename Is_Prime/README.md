# Prime Number Checking Methods

This document provides two different methods for checking whether a number is prime.

## 1. Iteration Method (Recursive Approach)
This method checks divisibility using recursion:
- If the number is 1 or less, it returns `False` (not prime).
- If the divisor equals the number, it returns `True` (it is prime).
- If the number is divisible by the divisor, it returns `False`.
- Otherwise, it recursively checks the next divisor.

### Code:
```python
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
```

## 2. Square Root Method (Efficient Approach)
This method optimizes prime checking by only testing divisibility up to the square root of the number:
- If the number is 1 or less, it returns `False`.
- It checks divisibility for all numbers from `2` to `sqrt(n)`.
- If any number divides evenly, it returns `False`.

### Code:
```python
def is_prime(number):
    if number <= 1:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True

num = int(input("Enter a number: "))

if is_prime(num):
    print(f"{num} is a prime number.")
else:
    print(f"{num} is not a prime number.")
```

## Comparison:
| Method         | Efficiency | Best For |
|---------------|-----------|----------|
| Iteration (Recursion) | Less efficient (O(n)) | Understanding recursion |
| Square Root  | More efficient (O(sqrt(n))) | Faster execution |

The square root method is generally recommended for better performance.

