import time
import random
import re
from datetime import datetime
from typing import TYPE_CHECKING

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    
except ImportError:
    webdriver = None  # allows fallback

if TYPE_CHECKING:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager


HASHTAGS = ["nifty50", "sensex", "intraday", "banknifty"]
TARGET_TWEETS = 50
MAX_SCROLLS = 3


def scrape_all_hashtags():
    if webdriver is None:
        print("[WARN] Selenium not available. Skipping live scraping.")
        return []

    all_tweets = []

    for tag in HASHTAGS:
        print(f"[INFO] Attempting live scrape for #{tag}")
        try:
            tag_tweets = scrape_hashtag(tag)
            all_tweets.extend(tag_tweets)
        except Exception as e:
            print(f"[WARN] Live scraping failed for #{tag}: {e}")

    return all_tweets


def scrape_hashtag(hashtag: str):
    if webdriver is None:
        raise RuntimeError("Selenium not available")

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    url = f"https://twitter.com/search?q=%23{hashtag}&f=live"
    driver.get(url)
    time.sleep(6)

    collected = {}
    scrolls = 0

    while len(collected) < TARGET_TWEETS and scrolls < MAX_SCROLLS:
        tweets = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")

        for tweet in tweets:
            try:
                content = tweet.text
                timestamp = datetime.utcnow().isoformat()
                tweet_id = hash(content + timestamp)

                collected[tweet_id] = {
                    "username": "unknown",
                    "timestamp": timestamp,
                    "content": content,
                    "likes": 0,
                    "retweets": 0,
                    "replies": 0,
                    "mentions": re.findall(r"@\w+", content),
                    "hashtags": re.findall(r"#\w+", content),
                    "scraped_at": timestamp,
                    "source_hashtag": hashtag
                }
            except Exception:
                continue

        driver.execute_script("window.scrollBy(0, 1500)")
        time.sleep(random.uniform(2, 4))
        scrolls += 1

    driver.quit()
    return list(collected.values())
