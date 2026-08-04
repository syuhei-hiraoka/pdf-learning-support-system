from tfidf import run_tfidf
from feature_builder import FeatureBuilder
from collections import defaultdict
from BM25_files import BM25
from vector_search import VectorSearch
from search_types import (
    QueryWords,
    JoinedDocs,
    SearchResults,
    SearchScores,
    BM25_TITLE,
    TFIDF_TITLE,
    VECTOR_TITLE,
    HYBRID_TITLE,
    RRF_TITLE,
    BM25_VECTOR_HYBRID_TITLE,
    LTR_TITLE,
)


LTR_SEARCH_METHODS = (
    BM25_TITLE,
    TFIDF_TITLE,
    VECTOR_TITLE,
    RRF_TITLE,
)


def make_rrf_inputs(
    query: QueryWords,
    bm25: BM25,
    joined_docs: JoinedDocs,
    vector: VectorSearch,
) -> SearchResults:
    """
    RRFの入力する検索結果を生成する。
    
    Parameters
    ----------
    query : QueryWords
        前処理後の検索語。
    bm25 : BM25
        BM25検索器。
    joined_docs : JoinedDocs
        PDFの全文。
    vector : VectorSearch
        ベクトル検索器。
    
    Returns
    -------
    SearchResults
        RRFに入れる検索結果。
    """
    return {
        BM25_TITLE: bm25.search(query),
        TFIDF_TITLE: run_tfidf(
            joined_docs,
            " ".join(query)
        ),
        VECTOR_TITLE: vector.search(query),
    }
    
def make_ltr_inputs(
    results: SearchResults,
    rrf_results: SearchScores,
) -> dict[int, dict[str, float]]:
    """
    各検索スコアをdoc_idごとに統合する。
    
    LTRが扱いやすい特徴形式に変換する。
    
    Parameters
    ----------
    results : SearchResults
        各検索器の検索結果。
    rrf_results : SearchScores
        RRFの検索結果。
    
    Returns
    -------
    dict[int, dict[str, float]]
        各検索器の検索結果をdoc_idごとにまとめ辞書型にする。
    """
    
    scores = defaultdict(
        lambda: {
            method: 0.0
            for method in LTR_SEARCH_METHODS
        }
    )
    
    for method, result in results.items():
        for (doc_id, score) in result:
            scores[doc_id][method] = score
    
    for doc_id, score in rrf_results:
        scores[doc_id][RRF_TITLE] = score
        
    return dict(scores)

def search_all(
    query: QueryWords, 
    resources: "SearchResources",
) -> SearchResults:
    """
    すべての検索エンジンで検索を実行する。
    
    Parameters
    ----------
    query : QueryWords
        前処理後の検索語。
    resources : SearchResources
        検索に必要なリソース。
    
    Returns
    -------
    SearchResults
        各検索手法の検索結果。
    """
    
    rrf_inputs = make_rrf_inputs(
            query,
            resources.bm25,
            resources.joined_docs,
            resources.vector,
        )
    
    hybrid_results = resources.search_engine.search(
        query,
        alpha=resources.hybrid_best_alpha
    )
    
    rrf_results = resources.rrf.search(rrf_inputs)
    
    bm25_vector_results = resources.bm25_vector_hybrid.search(
        query,
        alpha=resources.bm25vector_best_alpha
    )
    
    builder = FeatureBuilder()
    ltr_inputs = make_ltr_inputs(rrf_inputs, rrf_results)
    features = builder.build(
        query,
        ltr_inputs,
        resources.body_texts,
        resources.pdf_files,
    )
    ltr_results = resources.ltr.predict(features)
    
    
    results = {
        BM25_TITLE:rrf_inputs[BM25_TITLE],
        TFIDF_TITLE:rrf_inputs[TFIDF_TITLE],
        VECTOR_TITLE:rrf_inputs[VECTOR_TITLE],
        HYBRID_TITLE:hybrid_results,
        RRF_TITLE:rrf_results,
        BM25_VECTOR_HYBRID_TITLE:bm25_vector_results,
        LTR_TITLE:ltr_results,
    }
    
    return results