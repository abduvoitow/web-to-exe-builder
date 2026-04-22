import webview
import sys
import os
import base64

# These will be replaced by the GitHub Action during build
TARGET_URL = "https://google.com"
APP_NAME = "WebToEXE App"

HTML_SHELL = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body, html {{
            margin: 0;
            padding: 0;
            height: 100%;
            overflow: hidden;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: #000;
        }}
        .top-bar {{
            height: 40px;
            background: rgba(30, 30, 30, 0.85);
            backdrop-filter: blur(10px);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 15px;
            color: #fff;
            user-select: none;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .drag-region {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            /* In pywebview, use this class for dragging */
        }}
        .nav-controls {{
            display: flex;
            gap: 12px;
            z-index: 10;
        }}
        .nav-btn {{
            cursor: pointer;
            opacity: 0.7;
            transition: opacity 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .nav-btn:hover {{
            opacity: 1;
        }}
        .nav-btn svg {{
            width: 18px;
            height: 18px;
            fill: #fff;
        }}
        .title-logo {{
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            font-size: 13px;
            font-weight: 500;
            letter-spacing: 0.5px;
            color: rgba(255, 255, 255, 0.9);
            pointer-events: none;
        }}
        .window-controls {{
            display: flex;
            gap: 15px;
            z-index: 10;
        }}
        .win-btn {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            cursor: pointer;
        }}
        .close {{ background: #ff5f56; }}
        .min {{ background: #ffbd2e; }}
        .max {{ background: #27c93f; }}
        
        iframe {{
            width: 100%;
            height: calc(100% - 40px);
            border: none;
            background: #fff;
        }}
    </style>
</head>
<body>
    <div class="top-bar pywebview-drag-region">
        <div class="nav-controls">
            <div class="nav-btn" onclick="goBack()" title="Back">
                <svg viewBox="0 0 24 24"><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/></svg>
            </div>
            <div class="nav-btn" onclick="goForward()" title="Forward">
                <svg viewBox="0 0 24 24"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>
            </div>
            <div class="nav-btn" onclick="reload()" title="Refresh">
                <svg viewBox="0 0 24 24"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>
            </div>
        </div>
        
        <div class="title-logo">{APP_NAME}</div>
        
        <div class="window-controls">
            <div class="win-btn min" onclick="pywebview.api.minimize()"></div>
            <div class="win-btn max" onclick="pywebview.api.maximize()"></div>
            <div class="win-btn close" onclick="pywebview.api.close()"></div>
        </div>
    </div>
    
    <iframe id="main-frame" src="{TARGET_URL}"></iframe>

    <script>
        const iframe = document.getElementById('main-frame');
        
        function goBack() {{ iframe.contentWindow.history.back(); }}
        function goForward() {{ iframe.contentWindow.history.forward(); }}
        function reload() {{ iframe.src = iframe.src; }}
    </script>
</body>
</html>
"""

class API:
    def __init__(self):
        self.window = None

    def close(self):
        self.window.destroy()

    def minimize(self):
        self.window.minimize()

    def maximize(self):
        self.window.toggle_fullscreen()

def start_webview():
    api = API()
    window = webview.create_window(
        APP_NAME, 
        html=HTML_SHELL,
        js_api=api,
        width=1280,
        height=720,
        resizable=True,
        min_size=(800, 600),
        frameless=True # This enables our custom title bar
    )
    api.window = window
    webview.start()

if __name__ == "__main__":
    start_webview()
