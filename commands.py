"""
commands.py - Skill functions: open apps, open browsers, search the web, time/date.

Keeps action logic separate from voice/LLM logic so new skills can be added
here without touching assistant_core.py or the command router.
"""
import subprocess
import webbrowser
import datetime
import platform

# Windows executable names for supported browsers.
# Extend this dict if you want more browsers (brave, opera, etc.)
BROWSER_EXECUTABLES = {
    "edge": "msedge",
    "chrome": "chrome",
    "firefox": "firefox",
}


def get_time() -> str:
    return datetime.datetime.now().strftime("%I:%M %p")


def get_date() -> str:
    return datetime.datetime.now().strftime("%B %d, %Y")


def open_app(app_name: str) -> bool:
    """Open a known desktop app by name. Returns True if launched successfully."""
    app_name = app_name.lower().strip()
    try:
        if platform.system() == "Windows":
            if "explorer" in app_name:
                subprocess.Popen(["explorer"])
                return True
            if app_name in BROWSER_EXECUTABLES:
                subprocess.Popen([BROWSER_EXECUTABLES[app_name]])
                return True
        else:
            # Basic Linux/Mac fallback - extend as needed
            if app_name in BROWSER_EXECUTABLES:
                subprocess.Popen([app_name])
                return True
    except FileNotFoundError:
        return False
    return False


def open_url(url: str, browser: str = None) -> bool:
    """Open a URL, in a specific browser if given, else system default."""
    try:
        if browser and platform.system() == "Windows" and browser in BROWSER_EXECUTABLES:
            subprocess.Popen([BROWSER_EXECUTABLES[browser], url])
            return True
        webbrowser.open(url)
        return True
    except Exception:
        return False


def search_web(query: str, browser: str = None) -> bool:
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    return open_url(url, browser)

def open_youtube(browser: str = None) -> bool:
    return open_url("https://www.youtube.com", browser)


def open_google(browser: str = None) -> bool:
    return open_url("https://www.google.com", browser)


def youtube_search(query: str, browser: str = None) -> bool:
    from urllib.parse import quote
    url = f"https://www.youtube.com/results?search_query={quote(query)}"
    return open_url(url, browser)

def spotify_play(query: str) -> bool:
    """
    No API key needed. Hands the search query straight to the Spotify
    desktop app via the spotify:search: URI scheme. The app opens with
    search results — user (or a future auto-click step) picks the track.
    Works regardless of Free/Premium account, no developer app required.
    Requires the Spotify desktop app to be installed.
    """
    from urllib.parse import quote
    try:
        webbrowser.open(f"spotify:search:{quote(query)}")
        return True
    except Exception:
        return False


def whatsapp_send(contact_name: str, message: str) -> tuple[bool, str]:
    """
    Resolves contact_name -> phone number via contacts.py, then sends via
    WhatsApp Web. Returns (success, reason) so the caller can give a
    specific spoken error instead of a flat "couldn't send".

    KNOWN FRAGILITY (test live before trusting this in front of anyone):
    - Requires web.whatsapp.com already logged in on your DEFAULT browser.
    - pywhatkit uses pyautogui to simulate an Enter keypress after
    wait_time seconds. If ANY other window (VS Code, terminal, another
    Chrome tab) has focus when that keypress fires, the Enter goes to
    the WRONG window and the WhatsApp message never sends — silently.
    Don't touch your keyboard/mouse during the wait_time window.
    - tab_close=True closes the tab right after — if your internet is

    number = contacts.resolve_contact(contact_name)
    if number is None:
        return False, f"I don't have a contact saved for {contact_name}, boss."

    try:
        import pywhatkit
        pywhatkit.sendwhatmsg_instantly(
            phone_no=number, message=message, wait_time=20, tab_close=True
        )
        return True, ""
    except Exception as e:
        return False, f"WhatsApp send failed: {e}"



def open_app(app_name: str) -> bool:
    """Open a known desktop app by name. Returns True if launched successfully."""
    app_name = app_name.lower().strip()
    try:
        if platform.system() == "Windows":
            if "explorer" in app_name:
                subprocess.Popen(["explorer"])
                return True
            if app_name in BROWSER_EXECUTABLES:
                subprocess.Popen([BROWSER_EXECUTABLES[app_name]])
                return True
            # Generic fallback: let Windows resolve installed apps via
            # PATH / registered "App Paths" (covers Spotify, VLC,
            # Notepad, Calculator, and most Start-Menu-installed apps
            # without needing a hardcoded per-app dict).
            subprocess.Popen(f'start "" {app_name}', shell=True)
            return True
        else:
            if app_name in BROWSER_EXECUTABLES:
                subprocess.Popen([app_name])
                return True
    except FileNotFoundError:
        return False
    return False