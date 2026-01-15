import numpy as np

def compute_sentiment_signal(tweets):

    scores= []
    for t in tweets:
        engagement= (t.get("likes", 0) + t.get("retweets", 0) * 2 + t.get("replies", 0))
        scores.append(engagement)

    if not scores:
        return 0.0, 0.0

    mean_signal = float(np.mean(scores))
    confidence = float(np.std(scores) / (mean_signal + 1))

    return mean_signal, confidence
