import webview
import sys
import os

# These will be replaced by the GitHub Action during build
TARGET_URL = "https://google.com"
APP_NAME = "WebToEXE App"

def start_webview():
    window = webview.create_window(
        APP_NAME, 
        url=TARGET_URL,
        width=1280, height=720,
        resizable=True, 
        frameless=False
    )
    
    webview.start(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')

if __name__ == "__main__":
    start_webview()
