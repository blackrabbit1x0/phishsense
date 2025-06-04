"""
Phishing Email Detector - Main Application
Entry point for the application that initializes the GUI
"""

import os
import sys
from custom_gui import PhishingDetectorApp

def main():
    """Main function to start the application"""
    app = PhishingDetectorApp()
    app.mainloop()

if __name__ == "__main__":
    main()