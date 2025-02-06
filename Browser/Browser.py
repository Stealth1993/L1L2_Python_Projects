from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Create a QWebEngineView widget
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.duckduckgo.com"))
        self.setCentralWidget(self.browser)

        # Show the window maximized
        self.showMaximized()

        # Create a navigation toolbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Add a back button
        back_btn = QAction("⮜", self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        # Add a forward button
        forward_btn = QAction("⮞", self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        # Add a reload button
        reload_btn = QAction("⟳", self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        # Add a URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.open_url)
        navbar.addWidget(self.url_bar)

        # Update URL bar when browser URL changes
        self.browser.urlChanged.connect(self.update_url)

        # Apply dark theme to UI
        self.apply_dark_theme()

        # Inject dark mode into web pages after loading
        self.browser.page().loadFinished.connect(self.inject_dark_mode)

    # Load URL entered in the URL bar
    def open_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

    # Update URL bar when the browser URL changes
    def update_url(self, q):
        self.url_bar.setText(q.toString())

    # Apply dark theme to UI
    def apply_dark_theme(self):
        dark_stylesheet = """
            QMainWindow {
                background-color: #2e2e2e;
            }
            QToolBar {
                background-color: #3a3a3a;
                color: #ffffff;
            }
            QLineEdit {
                background-color: #4a4a4a;
                color: #ffffff;
                border: 1px solid #5a5a5a;
            }
            QPushButton {
                background-color: #4a4a4a;
                color: #ffffff;
                border: 1px solid #5a5a5a;
            }
        """
        self.setStyleSheet(dark_stylesheet)

    # Inject JavaScript-based dark mode into web pages
    def inject_dark_mode(self):
        dark_mode_js = """
            (function() {
                let style = document.createElement('style');
                style.type = 'text/css';
                style.innerHTML = `
                    html, body {
                        background-color: #2e2e2e !important;
                        color: #ffffff !important;
                    }
                    a {
                        color: #bb86fc !important;
                    }
                    input, textarea {
                        background-color: #4a4a4a !important;
                        color: #ffffff !important;
                        border: 1px solid #5a5a5a !important;
                    }
                    img, video {
                        filter: brightness(0.8) contrast(1.2) !important;
                    }
                `;
                document.head.appendChild(style);
            })();
        """
        self.browser.page().runJavaScript(dark_mode_js)

# Run the app
app = QApplication(sys.argv)
QApplication.setApplicationName("EFFLUX Browser")
window = MainWindow()
app.exec_()
