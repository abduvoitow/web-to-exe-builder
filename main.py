import webview
import sys

# These will be replaced by the GitHub Action during build
TARGET_URL = "https://google.com"
APP_NAME = "WebToEXE App"

def start_webview():
    window = webview.create_window(
        APP_NAME, 
        TARGET_URL,
        width=1280,
        height=720,
        resizable=True,
        min_size=(800, 600)
    )
    webview.start()

if __name__ == "__main__":
    start_webview()
