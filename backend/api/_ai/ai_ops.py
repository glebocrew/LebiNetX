def ai_hashtags(text):
    from keybert import KeyBERT

    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(
        text, keyphrase_ngram_range=(1, 1), stop_words=None
    )
    return ["#" + k[0] for k in keywords[:3]]
