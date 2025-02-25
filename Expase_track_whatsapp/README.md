\*\*# WhatsApp Expense Tracker

## Overview

This Python script automatically fetches expenses from a WhatsApp group (**daily\_exp**) and calculates equal shares among participants.

## Features

- Reads messages from WhatsApp Web
- Extracts expense details from messages (e.g., *Romi: 500 Dinner*)
- Calculates how much each person owes or is owed
- Refreshes every 60 seconds to check for new messages

## How to Use

1. **Install Requirements:**
   ```bash
   pip install selenium
   ```
2. **Run the Script:**
   ```bash
   python whatsapp_expense_tracker.py
   ```
3. **Scan the QR Code** to log in to WhatsApp Web.
4. The script will automatically fetch and process expenses.

## Limitations

- Requires WhatsApp Web to be open.
- WhatsApp may block automated access over time.

## Future Improvements

- Integrate with WhatsApp Business API for direct message retrieval.
- Develop a mobile app for easy access.

---

**Author:** Santosh Jha

