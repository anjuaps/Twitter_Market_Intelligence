import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

BULLISH_TERMS=["buy", "bullish", "breakout", "support", "long", "uptrend", "gap up"]
BEARISH_TERMS= ["sell", "bearish", "breakdown", "resistance", "short", "downtrend", "gap down"]

def compute_lexicon_score(text: str) -> int:
    text= text.lower()
    bullish= sum(term in text for term in BULLISH_TERMS)
    bearish= sum(term in text for term in BEARISH_TERMS)
    return bullish - bearish

def generate_signals(parquet_path: str) -> pd.DataFrame:
    
    df= pd.read_parquet(parquet_path)

    vectorizer= TfidfVectorizer(max_features=3000, stop_words="english")

    tfidf_matrix= vectorizer.fit_transform(df["content"])
    tfidf_scores= tfidf_matrix.mean(axis=1).A1
    df["lexicon_score"]=df["content"].apply(compute_lexicon_score)
    df["engagement"]=df["likes"] + df["retweets"] + 1

    df["final_signal"]=(0.6 * tfidf_scores + 0.4 * df["lexicon_score"]) * np.log1p(df["engagement"])

    return df
