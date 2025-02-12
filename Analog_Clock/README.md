# ⏰ Analog Clock using Tkinter

A visually appealing **analog clock** built with Python's **Tkinter**! This clock features smooth real-time updates, elegant design, and a simple yet effective implementation.

---

## ✨ Features
✔️ Real-time updating clock ⏳  
✔️ Beautiful analog interface with hour, minute, and second hands 🕰️  
✔️ Numeric markers for clock hours (1-12) 🔢  
✔️ Lightweight and easy to run ⚡  

---

## 📌 Requirements
- **Python 3.x** 🐍  
- **Tkinter** (built-in with standard Python distribution) 🖼️  

---

## 🚀 Installation & Usage
1️⃣ Ensure Python is installed on your system.  
2️⃣ Download or copy the `analog_clock.py` file.  
3️⃣ Run the script with the command:
   ```sh
   python analog_Clock_with_sys_time.py
   ```
4️⃣ The **analog clock** window will open and display the current time! 🎉  

---

## 🔍 How It Works
- The script **calculates the angles** of the hour, minute, and second hands based on the current time.  
- Uses **trigonometry** (`sin` and `cos` functions) for precise hand movement.  
- The **Canvas widget** renders the clock face, numbers, and hands.  
- The clock updates every **second** using Tkinter’s `after()` method.  

---

## 🛠️ Code Breakdown
🔹 `update_clock()`: Fetches the current time, calculates angles, and redraws the clock.  
🔹 `draw_hand()`: Draws the clock hands dynamically based on calculated angles.  
🔹 Tkinter’s **Canvas** is used to create the clock face and elements.  

---

## 🖼️ Screenshot
*(You can add a screenshot of the clock UI here)*  

---

## 📜 License
This project is **open-source** and available under the **MIT License**.  

🕰️ **Enjoy your analog clock!** ⏳

