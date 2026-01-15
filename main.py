import json

from processing.cleaner import clean_text
from processing.deduplicator import TweetDeduplicator
from storage.parquet_writer import write_tweets_to_parquet
from analysis.vectorizer import build_tfidf_matrix
from analysis.signal_aggregator import compute_sentiment_signal


USE_LIVE_SCRAPING = False


def load_offline_data(path="data/raw/tweets.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    print("Starting Twitter Market Intelligence System")

    deduplicator = TweetDeduplicator()
    processed = []

    # DATA INGESTION 
    if USE_LIVE_SCRAPING:
        try:
            from scraper.twitter_scraper import scrape_all_hashtags
            tweets = scrape_all_hashtags()
        except Exception as e:
            print("[ERROR] Live scraping blocked:", str(e))
            print("[INFO] Falling back to offline dataset")
            tweets = load_offline_data()
    else:
        print("[INFO] Using offline captured tweets (creative mode)")
        tweets = load_offline_data()

    # PROCESSING
    for tweet in tweets:
        cleaned = clean_text(tweet["content"])
        tweet_id = hash(tweet["username"] + cleaned + tweet["timestamp"])

        if not deduplicator.is_duplicate(str(tweet_id)):
            tweet["content"] = cleaned
            processed.append(tweet)

    # ANALYSIS
    if processed:
        texts = [t["content"] for t in processed]
        tfidf_matrix, _ = build_tfidf_matrix(texts)
        signal, confidence = compute_sentiment_signal(processed)

        print(f"[SIGNAL] Market Activity Score: {signal:.2f}")
        print(f"[CONFIDENCE] Signal Confidence: {confidence:.2f}")
    else:
        print("[WARN] No tweets available for analysis")

    # STORAGE
    write_tweets_to_parquet(processed)
    print(f"[SUCCESS] Stored {len(processed)} unique tweets")


if __name__ == "__main__":
    main()
