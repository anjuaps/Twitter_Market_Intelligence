class TweetDeduplicator:
    def __init__(self):
        self.seen_tweets= set()

    def is_duplicate(self, tweet_id: str) -> bool:
        if tweet_id in self.seen_tweets:
            return True

        self.seen_tweets.add(tweet_id)
        return False
