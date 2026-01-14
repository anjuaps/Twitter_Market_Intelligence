import time
import random
import re
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


HASHTAGS= ["nifty50", "sensex", "intraday", "banknifty"]
TARGET_TWEETS= 2000 #design target (24h window)
MAX_SCROLLS= 30 #safe runtime limit for demo


def extract_engagement(text: str) -> int:
    match = re.search(r"(\d+)", text.replace(",", ""))
    return int(match.group(1)) if match else 0


def scrape_hashtag(hashtag: str):
    options= webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")

    driver= webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

    url= f"https://twitter.com/search?q=%23{hashtag}&f=live"
    driver.get(url)
    time.sleep(6)

    collected= {}
    scroll_count= 0

    while len(collected) < TARGET_TWEETS and scroll_count < MAX_SCROLLS:
        tweets= driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")

        for tweet in tweets:
            try:
                username= tweet.find_element(By.XPATH, ".//span[contains(text(),'@')]").text
                content= tweet.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
                timestamp= tweet.find_element(By.XPATH, ".//time").get_attribute("datetime")
                aria_labels= tweet.find_elements(By.XPATH, ".//div[@role='group']//span")
                likes= retweets= replies = 0

                for span in aria_labels:
                    label= span.get_attribute("aria-label")
                    if not label:
                        continue
                    if "Like" in label:
                        likes= extract_engagement(label)
                    elif "Retweet" in label:
                        retweets= extract_engagement(label)
                    elif "Reply" in label:
                        replies= extract_engagement(label)

                mentions= re.findall(r"@\w+", content)
                hashtags= re.findall(r"#\w+", content)

                tweet_id= hash(username + content + timestamp)

                collected[tweet_id]= {
                    "username": username,
                    "timestamp": timestamp,
                    "content": content,
                    "likes": likes,
                    "retweets": retweets,
                    "replies": replies,
                    "mentions": mentions,
                    "hashtags": hashtags,
                    "scraped_at": datetime.utcnow().isoformat(),
                    "source_hashtag": hashtag
                }

            except Exception:
                continue

        driver.execute_script("window.scrollBy(0, 1400)")
        time.sleep(random.uniform(2.5, 5.0))
        scroll_count+=1

    driver.quit()
    return list(collected.values())

def scrape_all_hashtags():
    all_tweets= []

    for tag in HASHTAGS:
        print(f"Scraping #{tag}...")
        tag_tweets= scrape_hashtag(tag)
        all_tweets.extend(tag_tweets)

    return all_tweets
