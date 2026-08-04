from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from search_types import (
    PdfFiles,
    SearchScores,
)

MIN_DF_THRESHOLD = 3


def create_vectorizer(num_docs: int) -> TfidfVectorizer:
    """
    文書数に応じたTF-IDFベクトライザを作成する。
    
    Parameters
    ----------
    num_docs : int
        文書数。
        
    Returns
    -------
    TfidfVectorizer
        TF-IDFベクトライザ。
    """
    if num_docs < MIN_DF_THRESHOLD:
        return TfidfVectorizer()
    return TfidfVectorizer(
        max_df=0.8, 
        min_df=2,
    )
    

def run_tfidf(documents: PdfFiles, query: str) -> SearchScores:
    """
    TF-IDFで全文検索を行う。
    
    Parameters
    ----------
    documents : PdfFiles
        PDF全文。
    query : str
        スペース区切りの検索語。
    
    Returns
    -------
    SearchScores
        スコア順に並んだ検索結果。
    """
    vectorizer = create_vectorizer(len(documents))

    tfidf_matrix = vectorizer.fit_transform(
        documents
    )
    
    query_vector = vectorizer.transform(
        [query]
    )

    similarities: list[float] = cosine_similarity(
        query_vector,
        tfidf_matrix
    )[0]

    results = sorted(
        enumerate(similarities),
        key=lambda result: result[1],
        reverse=True
    )

    return results