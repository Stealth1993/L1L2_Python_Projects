# NoGio Browser

NoGio Browser is a simple web browser built using **PyQt5** and **QtWebEngine**. It features a dark mode theme for both the UI and web pages.

## Features
✅ **Dark Mode UI** – Applies a dark theme to the browser interface.
✅ **Web Page Dark Mode** – Injects JavaScript to enforce dark mode on most websites.
✅ **Navigation Toolbar** – Includes Back, Forward, Reload, and URL bar.
✅ **Minimal & Lightweight** – Focused on simplicity and efficiency.

## Installation
### **1. Install Required Dependencies**
Ensure you have Python installed (Python 3.6+ recommended). Install **PyQt5** and **PyQtWebEngine**:
```sh
pip install PyQt5 PyQtWebEngine
```

### **2. Clone or Download the Repository**
```sh
git clone https://github.com/yourusername/efflux-browser.git
cd efflux-browser
```

### **3. Run the Browser**
```sh
python efflux_browser.py
```

## Usage
- Enter a **URL** in the address bar and press **Enter** to navigate.
- Use the **Back** (⮜), **Forward** (⮞), and **Reload** (⟳) buttons for navigation.
- The **dark mode** is automatically applied to web pages after they load.

## Known Issues
⚠ **Some websites with strict Content Security Policies (CSP)** may block the dark mode script.
⚠ **YouTube and Google work**, but certain sites might not support JavaScript injection.

## Future Improvements
- Customizable dark mode toggle.
- Bookmark support.
- Enhanced JavaScript injection for improved compatibility.

## License
This project is open-source and available under the **MIT License**.

---
Feel free to contribute and improve NoGio Browser! 🚀

