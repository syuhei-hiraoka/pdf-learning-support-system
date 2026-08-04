from typing import Protocol
from search_types import (
    QueryWords,
    SearchScores,
    PdfFiles,
)

DEBUG = False
ALPHA_CANDIDATES = [
    0.1, 0.2, 0.3,
    0.4, 0.5, 0.6, 
    0.7, 0.8, 0.9
]

class SearchEngine(Protocol):
    def search(
        self,
        query: QueryWords,
        alpha: float,
    ) -> SearchScores:
        ...

def optimizer_alpha(
    search_engine: SearchEngine, 
    test_queries: list[tuple[QueryWords, str]], 
    pdf_files: PdfFiles,
) -> float:
    """
    Hybrid検索の最適なalphaを探索する。
    
    テストクエリを用いて各alphaを評価し、
    最も正解数が多いalphaを返す。
    
    Parameters
    ----------
    search_engine : SearchEngine 
        alphaによる重み調整が可能な検索器。
    test_queries : list[tuple[QueryWords, str]]
        試験用の単語リスト。
    pdf_files : PdfFiles
        PDFファイル名一覧。
    
    Returns
    -------
    float
        最適化なalpha値。
    """
    
    best_alpha: float | None = None
    best_score: int = -1
    
    for alpha in ALPHA_CANDIDATES:
        score = 0
        
        for query, correct_doc in test_queries:
            results = search_engine.search(
                query=query,
                alpha=alpha
            )
            
            if not results:
                continue
            
            top_doc_id = results[0][0]
            predicted_file = pdf_files[top_doc_id]
            
            if predicted_file == correct_doc:
                score += 1
        if DEBUG:        
            print(f"alpha={alpha}: {score}")
        
        if score > best_score:
            best_score=score
            best_alpha=alpha
            
    return best_alpha