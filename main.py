import webview
import sys
import os

# These will be replaced by the GitHub Action during build
TARGET_URL = "https://google.com"
APP_NAME = "WebToEXE App"

# We use a base64 or f-string HTML shell. 
# This shell is loaded LOCALALLY, so it's always displayed.
# Inside it, we have our Topbar and the Iframe.
# web_security=False will allow this local shell to load ANY iframe.

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
            background: #111;
        }}
        #top-bar {{
            height: 40px;
            background: rgba(25, 25, 25, 0.98);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 15px;
            color: #fff;
            user-select: none;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            z-index: 100;
        }}
        .pywebview-drag-region {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
        }}
        .nav-controls {{
            display: flex;
            gap: 15px;
            z-index: 110;
        }}
        .nav-btn {{
            cursor: pointer;
            opacity: 0.7;
            transition: opacity 0.2s;
            display: flex;
            align-items: center;
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
            font-weight: 600;
            letter-spacing: 0.3px;
            color: rgba(255, 255, 255, 0.9);
            pointer-events: none;
        }}
        .window-controls {{
            display: flex;
            gap: 12px;
            z-index: 110;
            padding-right: 5px;
        }}
        .win-btn {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            cursor: pointer;
            border: none;
        }}
        .close {{ background: #ff5f56; }}
        .min {{ background: #ffbd2e; }}
        .max {{ background: #27c93f; }}
        
        #content-frame {{
            width: 100%;
            height: calc(100% - 40px);
            border: none;
            background: #fff;
        }}
    </style>
</head>
<body>
    <div id="top-bar" class="pywebview-drag-region">
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
            <div class="win-btn min" onclick="window.pywebview.api.minimize()"></div>
            <div class="win-btn max" onclick="window.pywebview.api.maximize()"></div>
            <div class="win-btn close" onclick="window.pywebview.api.close()"></div>
        </div>
    </div>
    
    <iframe id="content-frame" src="{TARGET_URL}"></iframe>

    <script>
        const iframe = document.getElementById('content-frame');
        
        function goBack() {{
            try {{
                iframe.contentWindow.history.back();
            }} catch(e) {{
                console.error("Navigation error: ", e);
            }}
        }}
        
        function goForward() {{
            try {{
                iframe.contentWindow.history.forward();
            }} catch(e) {{
                console.error("Navigation error: ", e);
            }}
        }}
        
        function reload() {{
            iframe.src = iframe.src;
        }}
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
    
    # WebView2 on Windows is the target engine. 
    # web_security=False disables X-Frame-Options/CSP checks for the local shell.
    window = webview.create_window(
        APP_NAME, 
        html=HTML_SHELL,
        js_api=api,
        width=1280,
        height=720,
        resizable=True,
        min_size=(800, 600),
        frameless=True,
        web_security=False 
    )
    api.window = window
    
    # Modern Chrome User-Agent to avoid bot blocking
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    
    webview.start(user_agent=user_agent)

if __name__ == "__main__":
    start_webview()
