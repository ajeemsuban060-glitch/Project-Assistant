"""
command_router.py - Classifies transcribed text into an intent + args
before it reaches the LLM. Only unmatched text falls through to Q&A.

This keeps deterministic actions (open app, search, time) fast and free
(no LLM call), and reserves the LLM for actual reasoning/Q&A.
"""
import re

EXIT_WORDS = {"stop", "exit", "quit", "shutdown", "goodbye"}
BROWSER_NAMES = ["edge", "chrome", "firefox"]

# Words to strip off the front of an extracted query, in order.
_FILLER_PREFIXES = ("and ", "search for ", "search ", "play ", "for ")


def _strip_fillers(s: str) -> str:
    s = s.strip()
    changed = True
    while changed:
        changed = False
        for filler in _FILLER_PREFIXES:
            if s.startswith(filler):
                s = s[len(filler):].strip()
                changed = True
    return s


def route(text: str) -> dict:
    """
    Returns a dict describing the intent:
    {"intent": "exit"}
    {"intent": "youtube_search", "query": str}
    {"intent": "spotify_play", "query": str}
    {"intent": "whatsapp_send", "contact": str, "message": str}
    {"intent": "open_search", "browser": str|None, "query": str}
    {"intent": "open_app", "target": str}
    {"intent": "get_time"}
    {"intent": "get_date"}
    {"intent": "qa", "text": str}
    {"intent": "empty"}

    IMPORTANT: site-specific intents (youtube/spotify/whatsapp) MUST be
    checked before the generic "open X and search for Y" pattern below,
    because that pattern greedily swallows "youtube"/"spotify" as if it
    were a browser name and misroutes to a plain Google search.
    """
    t = text.lower().strip()

    if not t:
        return {"intent": "empty"}

    if any(w in t.split() for w in EXIT_WORDS):
        return {"intent": "exit"}

    # --- YouTube: "open youtube and search for X" / "play X on youtube" ---
    if "youtube" in t:
        m = re.search(r"(.+) on youtube", t)
        query = _strip_fillers(m.group(1)) if m else _strip_fillers(re.sub(r".*youtube\b", "", t))
        if query:
            return {"intent": "youtube_search", "query": query}
        return {"intent": "open_app", "target": "youtube"}

    # --- Spotify: "play X on spotify" / "spotify play X" ---
    if "spotify" in t:
        m = re.search(r"play (.+) on spotify", t)
        query = _strip_fillers(m.group(1)) if m else _strip_fillers(re.sub(r".*spotify\b", "", t))
        if query:
            return {"intent": "spotify_play", "query": query}
        return {"intent": "open_app", "target": "spotify"}

    # --- WhatsApp: "send whatsapp message to X saying Y" / "whatsapp X Y" ---
    m = re.search(r"whatsapp message to (\w+) saying (.+)", t)
    if not m:
        m = re.search(r"whatsapp (\w+) (?:that |saying )?(.+)", t)
    if m:
        return {"intent": "whatsapp_send", "contact": m.group(1).strip(), "message": m.group(2).strip()}

    # "open edge and search for top 10 ai models in world"
    m = re.search(r"open (\w+).*search for (.+)", t)
    if m:
        browser = m.group(1) if m.group(1) in BROWSER_NAMES else None
        return {"intent": "open_search", "browser": browser, "query": m.group(2).strip()}

    # "search for X" with no browser named -> use default browser
    m = re.search(r"search for (.+)", t)
    if m:
        return {"intent": "open_search", "browser": None, "query": m.group(1).strip()}

    # "open <app name>" / "open file explorer"
    m = re.search(r"open (.+)", t)
    if m:
        return {"intent": "open_app", "target": m.group(1).strip()}

    if "time" in t:
        return {"intent": "get_time"}
    if "date" in t:
        return {"intent": "get_date"}

    # Nothing matched -> treat as a question for the LLM
    return {"intent": "qa", "text": text}
    # "open edge and search for top 10 ai models in world"
    m = re.search(r"open (\w+).*search for (.+)", t)
    if m:
        browser = m.group(1) if m.group(1) in BROWSER_NAMES else None
        return {"intent": "open_search", "browser": browser, "query": m.group(2).strip()}

    # "search for X" with no browser named -> use default browser
    m = re.search(r"search for (.+)", t)
    if m:
        return {"intent": "open_search", "browser": None, "query": m.group(1).strip()}

    # "open youtube" / "open edge" / "open file explorer"
    m = re.search(r"open (.+)", t)
    if m:
        return {"intent": "open_app", "target": m.group(1).strip()}

    if "time" in t:
        return {"intent": "get_time"}
    if "date" in t:
        return {"intent": "get_date"}

    # Nothing matched -> treat as a question for the LLM
    return {"intent": "qa", "text": text}