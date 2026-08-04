from tfidf import run_tfidf
from resources import SearchResources
from .display import print_evaluation_results
from .metrics import METRIC_NAMES
from search import (
    make_rrf_inputs,
    make_ltr_inputs,
)
from search_types import (
    QueryWords,
    SearchScores,
    PdfFiles,
    AnswerFiles,
    SearchFunction,
    MetricFunction,
    SearchMethods,
    EvaluationResults,
)
from feature_builder import FeatureBuilder
    
DEFAULT_K = 5
    
def evaluate_search(
    search_function: SearchFunction,
    metric_function: MetricFunction,
    test_queries: list[tuple[QueryWords, AnswerFiles]],
    pdf_files: PdfFiles,
    k: int = DEFAULT_K,
) -> float:
    """
    検索手法を選択した評価指標で評価する。
    
    Parameters
    ----------
    search_function : SearchFunction
        検索語から検索結果を返す関数。
    metric_function : MetricFunction
        評価指標を計算する関数。
    test_queries : list[tuple[QueryWords, AnswerFiles]]
        試験用の検索語一覧。
    pdf_files : PdfFiles
        PDFファイル名一覧。
    k : int
        抽出した件数。
    
    Returns
    -------
    float
        それぞれの検索手法のスコアの平均値。

    """
    
    scores = [
        metric_function(
            search_function(query.words),
            query.answers,
            pdf_files,
            k,
        )
        for query in test_queries
    ]
    
    if not scores:
        return 0.0
        
    return sum(scores) / len(scores)


def make_search_methods(
    resources: SearchResources,
    test_queries: list[tuple[QueryWords, AnswerFiles]],
) -> SearchMethods:
    """
    検索手法の生成。
    
    Parameters
    ----------
    resources : SearchResources
        検索に必要なリソース。
    test_queries : list[tuple[QueryWords, AnswerFiles]]
        試験用の検索語一覧。
    
    Returns
    -------
    SearchMethods
        各検索手法から抽出した結果。
    """
    
    builder = FeatureBuilder()
    
    return{
        "BM25": lambda q: resources.bm25.search(q),
        
        "TF-IDF": lambda q: run_tfidf(
            resources.joined_docs,
            " ".join(q),
        ),
        
        "Hybrid": lambda q: resources.search_engine.search(
            q,
            alpha=resources.hybrid_best_alpha,
        ),
        
        "Vector": lambda q: resources.vector.search(q),
        
        "RRF": lambda q: resources.rrf.search(
            make_rrf_inputs(q, resources.bm25, resources.joined_docs, resources.vector)
        ),
        
        "BM25+Vector": lambda q: resources.bm25_vector_hybrid.search(
            q,
            alpha=resources.bm25vector_best_alpha,
        ),
        
        "LTR": lambda q: search_ltr(
            q,
            resources,
        ),
    }
    
def evaluate_all(
    resources: SearchResources, 
    test_queries: list[tuple[QueryWords, AnswerFiles]],
    k: int = DEFAULT_K,
) -> None:
    """
    全検索手法 x 全評価指数を実行する。

    Parameters
    ----------
    resources : SearchResources
        検索に必要なリソース。
    test_queries : list[tuple[QueryWords, AnswerFiles]]
        試験用検索語の一覧。
    k : int
        抽出した件数。
    """

    search_methods = make_search_methods(resources, test_queries)


    results: EvaluationResults = {}

    for metric, metric_name in METRIC_NAMES.items():
        metric_scores: dict[str, float] = {}
        
        
        for method_name, search_func in search_methods.items():
            metric_scores[method_name] = evaluate_search(
                search_func,
                metric,
                test_queries,
                resources.pdf_files,
                k,
            )
            
        results[metric_name] = metric_scores
            
    print_evaluation_results(results,k)
    
def search_ltr(
    q: QueryWords,
    resources: SearchResources,
) -> SearchScores:
    
    rrf_inputs = make_rrf_inputs(
        q,
        resources.bm25,
        resources.joined_docs,
        resources. vector,
    )
    
    rrf_results = resources.rrf.search(rrf_inputs)
    
    ltr_inputs = make_ltr_inputs(
        rrf_inputs,
        rrf_results,
    )
    
    builder = FeatureBuilder()
    
    features = builder.build(
        q,
        ltr_inputs,
        resources.body_texts,
        resources.pdf_files,
    )
    
    return resources.ltr.predict(features)