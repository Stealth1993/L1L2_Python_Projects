from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
from collections import defaultdict

# WhatsApp Web Automation Setup
def open_whatsapp():
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=./whatsapp_data")  # Keeps you logged in
    driver = webdriver.Chrome(options=options)
    driver.get("https://web.whatsapp.com/")
    input("Press Enter after scanning QR code...")
    return driver

def get_messages_from_group(driver, group_name="daily_exp"):
    """
    Fetches latest messages from the specified WhatsApp group.
    """
    search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
    search_box.clear()
    search_box.send_keys(group_name)
    time.sleep(2)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

    messages = driver.find_elements(By.XPATH, "//div[contains(@class, '_21Ahp')]")
    return [msg.text for msg in messages[-10:]]  # Get the last 10 messages

def parse_expenses(messages):
    """
    Extracts expenses from WhatsApp messages.
    Expected format: 'Name: Amount Item'
    """
    expenses = defaultdict(float)
    total_expense = 0

    for msg in messages:
        match = re.search(r"(\w+):\s*(\d+)\s*(.*)", msg)
        if match:
            person, amount, item = match.groups()
            amount = float(amount)
            expenses[person] += amount
            total_expense += amount

    return expenses, total_expense

def calculate_share(expenses, total_expense):
    """
    Calculates the equal share for each person.
    """
    num_people = len(expenses)
    if num_people == 0:
        print("No expenses found.")
        return {}

    equal_share = total_expense / num_people
    balances = {person: round(expenses[person] - equal_share, 2) for person in expenses}

    return balances

def main():
    driver = open_whatsapp()
    
    while True:
        print("\nFetching latest expenses...")
        messages = get_messages_from_group(driver, "daily_exp")
        expenses, total_expense = parse_expenses(messages)

        print("\n--- Expenses Recorded ---")
        for person, amount in expenses.items():
            print(f"{person}: {amount} currency units")

        print(f"\nTotal Expense: {total_expense} currency units")
        
        balances = calculate_share(expenses, total_expense)

        print("\n--- Settlement Details ---")
        for person, balance in balances.items():
            if balance > 0:
                print(f"{person} should receive {balance}")
            elif balance < 0:
                print(f"{person} should pay {-balance}")
            else:
                print(f"{person} is settled")

        time.sleep(60)  # Refresh every 60 seconds

if __name__ == "__main__":
    main()
