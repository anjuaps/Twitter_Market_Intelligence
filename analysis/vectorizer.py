from sklearn.feature_extraction.text import TfidfVectorizer

def build_tfidf_matrix(texts):
    vectorizer= TfidfVectorizer(max_features=3000, stop_words="english", ngram_range=(1, 2))

    tfidf_matrix= vectorizer.fit_transform(texts)
    return tfidf_matrix, vectorizer
