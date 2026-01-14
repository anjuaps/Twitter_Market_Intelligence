from processing.cleaner import clean_text
from processing.deduplicator import TweetDeduplicator


def main():
    print("Starting Twitter Market Intelligence System")
    raw_tweet= "🚀 BUY BankNifty breakout now! https://t.co/test"

    cleaned_tweet= clean_text(raw_tweet)
    print("Cleaned Tweet:", cleaned_tweet)

    deduplicator= TweetDeduplicator()
    tweet_id= hash(cleaned_tweet)

    if deduplicator.is_duplicate(str(tweet_id)):
        print("Duplicate tweet detected")
    else:
        print("New tweet processed")

if __name__== "__main__":
    main()


