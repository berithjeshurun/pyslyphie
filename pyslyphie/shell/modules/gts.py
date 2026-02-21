"""
Global Tracking System v2.0 (Non-CLI Version)
Author: Refactor based on GliTCH original
"""

import asyncio
import aiohttp
import re
import sys
import os
import json
import shelve
from urllib.parse import unquote
from datetime import datetime
from typing import List, Dict, Optional

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0 Safari/537.36"
DEFAULT_CONCURRENCY = 6
REQUEST_TIMEOUT = 20
RETRY_ATTEMPTS = 2
RETRY_BACKOFF = 1.25


domain_patterns_raw = {
    'Allibaba' : r'alibaba\.com',
    'Amazon'   : r'amazon\.com',
    'BBC'    : r'(bbc\.com/news|bbc\.com)',
    'Cambridge' : r'cambridge\.org',
    'Ebay' : r'ebay\.com',
    'Elblearning' : r'elblearning\.com',
    "Etsy" : r'etsy\.com',
    'Facebook': r'facebook\.com',
    'How it Works' : r'howstuffworks\.com',
    'Huff Post'    : r'huffpost\.com',
    'India Mart' : r'dir\.indiamart\.com',
    'Instagram': r'instagram\.com',
    'Linkedin' : r'linkedin\.com',
    'Marvel Fandom' : r'marvel\.fandom\.com',
    'NGC'  : r'nationalgeographic\.com',
    'Ngpf' : r'ngpf\.org',
    'Quora' : r'quora\.com',
    'Reddit' : r'reddit\.com',
    'Twitter': r'twitter\.com',
    'Xbox'   : r'marketplace\.xbox\.com',
    'Walmart' : r'walmart\.com',
    'Wikipedia' : r'wikipedia\.org',
    'Youtube': r'(youtube\.com|youtu\.be)',
    'Coursera' : r'coursera\.org',
    'Khanacademy' : r'khanacademy\.org',
    'Edx' : r'edx\.org',
    'Udemy'       : r'udemy\.com',
    'Codecademy'  : r'codecademy\.com',
    'Netflix'     : r'netflix\.com',
    'Imdb' : r'imdb\.com',
    'Spotify' : r'spotify\.com',
    'Apple' : r'apple\.com',
    'Google' : r'google\.com',
    'Microsoft' : r'microsoft\.com',
    'Tesla' : r'tesla\.com',
    'Govt : USA' : r'usa\.gov',
    'Govt : UK'  : r'gov\.uk',
    'Govt : Australia' : r'australia\.gov\.au',
    'Govt : Canada' : r'canada\.ca',
    'Govt : India' : r'india\.gov\.in',
    'Twitch' : r'twitch\.tv',
    'Flipkart' : r'flipkart\.com'
}

category_tags_raw = {
    "Business": [r'apple\.com', r'google\.com', r'microsoft\.com', r'tesla\.com'],
    "Community": [r'quora\.com', r'reddit\.com'],
    "Educational": [r'cambridge\.org', r'elblearning\.com', r'codecademy\.com', r'udemy\.com', r'edx\.org', r'khanacademy\.org', r'coursera\.org'],
    "E-Commerce": [r'alibaba\.com', r'amazon\.com', r'ebay\.com', r'etsy\.com', r'dir\.indiamart\.com', r'walmart\.com', r'flipkart\.com'],
    "Finance": [r'ngpf\.org'],
    "Films": [r'marvel\.fandom\.com', r'imdb\.com'],
    "Games": [r'marketplace\.xbox\.com'],
    "Government": [r'australia\.gov\.au', r'canada\.ca', r'india\.gov\.in', r'gov\.uk', r'usa\.gov'],
    "Informational": [r'bbc\.com', r'howstuffworks\.com', r'huffpost\.com', r'nationalgeographic\.com', r'wikipedia\.org'],
    "Marketing": [r'dir\.indiamart\.com'],
    "Social Media": [r'youtube\.com|youtu\.be', r'twitter\.com', r'facebook\.com', r'instagram\.com', r'linkedin\.com', r'twitch\.tv'],
    "Streaming": [r'netflix\.com', r'spotify\.com']
}

domain_patterns = {k: re.compile(v, re.IGNORECASE) for k, v in domain_patterns_raw.items()}
category_tags = {k: [re.compile(p, re.IGNORECASE) for p in patterns] for k, patterns in category_tags_raw.items()}

google_redirect_patterns = [
    re.compile(r'url\?q=(https?://[^&"\']+)', re.IGNORECASE),
    re.compile(r'/url\?sa=[^&]*&url=(https?://[^&"\']+)', re.IGNORECASE),
    re.compile(r'(https?://[^\s"\'<>]+)')
]

IGNORE_SUBSTRINGS = ("googleusercontent", "/settings/ads", "/policies/faq")

def decode_url(u: str) -> str:
    prev = None
    cur = u
    for _ in range(6):
        prev = cur
        cur = unquote(cur)
        if cur == prev:
            break
    return cur

def classify_url(url: str) -> Dict[str, Optional[str]]:
    platform = None
    category = None

    for name, patt in domain_patterns.items():
        if patt.search(url):
            platform = name
            break

    for cat, plist in category_tags.items():
        for p in plist:
            if p.search(url):
                category = cat
                break
        if category:
            break

    return {"platform": platform, "category": category}

class GlobalTracker:
    def __init__(self, concurrency=DEFAULT_CONCURRENCY, user_agent=USER_AGENT, cache_file=None):
        self.sem = asyncio.Semaphore(concurrency)
        self.headers = {"User-Agent": user_agent}
        self.cache_file = cache_file
        self.cache = shelve.open(cache_file) if cache_file else None

    async def _fetch(self, session, url):
        attempt = 0
        while attempt <= RETRY_ATTEMPTS:
            try:
                async with self.sem:
                    async with session.get(url, headers=self.headers, timeout=REQUEST_TIMEOUT) as r:
                        return await r.text(errors='ignore')
            except:
                attempt += 1
                await asyncio.sleep(RETRY_BACKOFF * attempt)
        return None

    def _extract(self, html):
        result = set()
        if not html:
            return []
        for patt in google_redirect_patterns:
            for u in patt.findall(html):
                u = decode_url(u)
                if any(bad in u for bad in IGNORE_SUBSTRINGS):
                    continue
                result.add(u)
        return list(result)

    async def search(self, query, num=100):
        key = f"{query}:{num}"
        if self.cache and key in self.cache:
            return list(self.cache[key])

        queries = [
            f"https://www.google.com/search?num={num}&q={query}",
            f"https://www.google.com/search?num={num}&q=intitle:\"{query}\""
        ]

        out = set()
        async with aiohttp.ClientSession() as s:
            pages = await asyncio.gather(*[self._fetch(s, q) for q in queries])

        for page in pages:
            for u in self._extract(page):
                out.add(u)

        out = list(out)
        if self.cache:
            self.cache[key] = out
            self.cache.sync()

        return out

    async def classify(self, urls):
        out = {}
        for u in urls:
            info = classify_url(u)
            out.setdefault(info["platform"] or "<Unknown>", []).append(u)
        return out

    def close(self):
        if self.cache:
            self.cache.close()

def run_tracker(
    username: str,
    num: int = 100,
    concurrency: int = DEFAULT_CONCURRENCY,
    cache_file: Optional[str] = None,
    save_json: Optional[str] = None
):
    """
    Main public entrypoint.

    Returns:
        {
            "query": username,
            "urls": [...],
            "classified": {...},
            "log_path": "..."
        }
    """
    tracker = GlobalTracker(concurrency=concurrency, cache_file=cache_file)

    async def _run():
        urls = await tracker.search(username, num)
        classified = await tracker.classify(urls)
        return urls, classified

    urls, classified = asyncio.run(_run())

    now = datetime.now()
    date_dir = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%Hh-%Mm-%Ss")

    log_dir = f"./logs/{date_dir}"
    os.makedirs(log_dir, exist_ok=True)
    log_path = f"{log_dir}/{time_str}.log"

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"[INFO] Generated on {date_dir} at {time_str}\n")
        f.write(f"[QUERY] {username}\n\n")
        for u in urls:
            f.write(u + "\n")

    if save_json:
        with open(save_json, "w", encoding="utf-8") as jf:
            json.dump({
                "query": username,
                "generated": now.isoformat(),
                "urls": urls,
                "classified": classified
            }, jf, indent=2)

    tracker.close()

    return {
        "query": username,
        "urls": urls,
        "classified": classified,
        "log_path": log_path
    }
