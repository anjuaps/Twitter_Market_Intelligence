from processing.cleaner import clean_text
from processing.deduplicator import TweetDeduplicator
from scraper.twitter_scraper import scrape_all_hashtags
from storage.parquet_writer import write_tweets_to_parquet

def main():
    print("Starting Twitter Market Intelligence System")

    deduplicator= TweetDeduplicator()
    processed= []

    tweets= scrape_all_hashtags()

    for tweet in tweets:
        cleaned= clean_text(tweet["content"])
        tweet_id= hash(tweet["username"]+cleaned+tweet["timestamp"])

        if not deduplicator.is_duplicate(str(tweet_id)):
            tweet["content"]=cleaned
            processed.append(tweet)

    write_tweets_to_parquet(processed)

if __name__ == "__main__":
    main()
