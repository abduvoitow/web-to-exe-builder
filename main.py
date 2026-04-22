import webview
import sys
import os
import time

# These will be replaced by the GitHub Action during build
TARGET_URL = "https://google.com"
APP_NAME = "WebToEXE App"

# CSS for our custom top bar
TOOLBAR_CSS = """
    #pywebview-topbar {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 40px;
        background: rgba(30, 30, 30, 0.95);
        backdrop-filter: blur(10px);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 15px;
        color: #fff;
        z-index: 2147483647;
        box-sizing: border-box;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        user-select: none;
    }
    .pywebview-drag-region {
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        z-index: -1;
    }
    .nav-controls { display: flex; gap: 15px; z-index: 10; }
    .nav-btn { cursor: pointer; opacity: 0.7; transition: 0.2s; display: flex; align-items: center; }
    .nav-btn:hover { opacity: 1; }
    .nav-btn svg { width: 18px; height: 18px; fill: #fff; }
    .title-logo { 
        position: absolute; left: 50%; transform: translateX(-50%);
        font-size: 13px; font-weight: 500; color: rgba(255, 255, 255, 0.9);
        pointer-events: none;
    }
    .window-controls { display: flex; gap: 12px; z-index: 10; padding-right: 25px; }
    .win-btn { width: 12px; height: 12px; border-radius: 50%; cursor: pointer; }
    .close { background: #ff5f56; }
    .min { background: #ffbd2e; }
    .max { background: #27c93f; }
    
    /* Push content down so it doesn't hide behind our bar */
    html, body { margin-top: 40px !important; }
"""

# HTML for our custom top bar
TOOLBAR_HTML = f"""
    <div id="pywebview-topbar" class="pywebview-drag-region">
        <div class="nav-controls">
            <div class="nav-btn" onclick="history.back()" title="Back">
                <svg viewBox="0 0 24 24"><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/></svg>
            </div>
            <div class="nav-btn" onclick="history.forward()" title="Forward">
                <svg viewBox="0 0 24 24"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>
            </div>
            <div class="nav-btn" onclick="location.reload()" title="Refresh">
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

def inject_ui(window):
    # This function injects the UI into the loaded page
    # Escape single quotes and backticks for safety in JS string
    css = TOOLBAR_CSS.replace('`', '\\`').replace('$', '\\$')
    html = TOOLBAR_HTML.replace('`', '\\`').replace('$', '\\$')
    
    js = f"""
        (function() {{
            if (document.getElementById('pywebview-topbar')) return;
            
            // Add Styles
            var style = document.createElement('style');
            style.id = 'pywebview-styles';
            style.innerHTML = `{css}`;
            document.head.appendChild(style);
            
            // Add HTML
            var div = document.createElement('div');
            div.innerHTML = `{html}`;
            document.body.insertBefore(div, document.body.firstChild);
        }})();
    """
    window.run_js(js)

def start_webview():
    api = API()
    window = webview.create_window(
        APP_NAME, 
        url=TARGET_URL,
        js_api=api,
        width=1280,
        height=720,
        resizable=True,
        min_size=(800, 600),
        frameless=True 
    )
    api.window = window
    
    # Inject UI when any page finishes loading
    window.events.loaded += lambda: inject_ui(window)
    
    webview.start()

if __name__ == "__main__":
    start_webview()
