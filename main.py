import webview
import sys
import os
import time

# These will be replaced by the GitHub Action during build
TARGET_URL = "https://google.com"
APP_NAME = "WebToEXE App"

TOOLBAR_CSS = """
    #pywebview-topbar {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 40px !important;
        background: rgba(20, 20, 20, 0.98) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        padding: 0 15px !important;
        color: #fff !important;
        z-index: 2147483647 !important;
        box-sizing: border-box !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        user-select: none !important;
    }
    .pywebview-drag-region {
        position: absolute !important;
        width: 100% !important;
        height: 100% !important;
        top: 0 !important;
        left: 0 !important;
        z-index: -1 !important;
    }
    .nav-controls { display: flex !important; gap: 15px !important; z-index: 10 !important; }
    .nav-btn { cursor: pointer !important; opacity: 0.7 !important; transition: 0.2s !important; display: flex !important; align-items: center !important; }
    .nav-btn:hover { opacity: 1 !important; }
    .nav-btn svg { width: 18px !important; height: 18px !important; fill: #fff !important; }
    .title-logo { 
        position: absolute !important; left: 50% !important; transform: translateX(-50%) !important;
        font-size: 13px !important; font-weight: 500 !important; color: rgba(255, 255, 255, 0.9) !important;
        pointer-events: none !important;
    }
    .window-controls { display: flex !important; gap: 12px !important; z-index: 10 !important; padding-right: 10px !important; }
    .win-btn { width: 12px !important; height: 12px !important; border-radius: 50% !important; cursor: pointer !important; border: none !important; }
    .close { background: #ff5f56 !important; }
    .min { background: #ffbd2e !important; }
    .max { background: #27c93f !important; }
    
    html, body { padding-top: 40px !important; }
"""

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
        # On windows, toggle_fullscreen acts like maximize for frameless
        self.window.toggle_fullscreen()

def inject_ui(window):
    css = TOOLBAR_CSS.replace('\n', ' ').replace('`', '\\`').replace('$', '\\$')
    html = TOOLBAR_HTML.replace('\n', ' ').replace('`', '\\`').replace('$', '\\$')
    
    js = f"""
        (function() {{
            function tryInject() {{
                if (document.getElementById('pywebview-topbar')) return;
                if (!document.body || !document.head) return;

                // Add Styles
                var style = document.getElementById('pywebview-styles');
                if (!style) {{
                    style = document.createElement('style');
                    style.id = 'pywebview-styles';
                    style.innerHTML = `{css}`;
                    document.head.appendChild(style);
                }}
                
                // Add HTML
                var div = document.createElement('div');
                div.innerHTML = `{html}`;
                document.body.insertBefore(div, document.body.firstChild);
                
                // Ensure body padding
                document.body.style.paddingTop = '40px';
                document.documentElement.style.paddingTop = '0px';
            }}

            // Try immediately and then every 500ms to catch dynamic changes
            tryInject();
            setInterval(tryInject, 1000);
        }})();
    """
    try:
        window.run_js(js)
    except:
        pass

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
        frameless=True,
        text_select=True,
        confirm_close=True
    )
    api.window = window
    
    # Run injection on load and every few seconds
    window.events.loaded += lambda: inject_ui(window)
    
    webview.start(debug=False)

if __name__ == "__main__":
    start_webview()
