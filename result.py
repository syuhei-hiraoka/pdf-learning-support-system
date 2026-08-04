from dataclasses import dataclass
from highlight import (
    highlight_text,
    select_best_highlight,
)
from resources import SearchResources
from search_types import (
    SearchScores,
    QueryWords,
)

@dataclass
class SearchResult:
    """
    検索結果を表すデータクラス。
    
    Parameters
    ----------
    rank : int
        検索順位。
    filename : str
        PDFファイル名。
    score : float
        検索スコア。
    page : int | None
        ヒットしたページ番号。
    snippet : str
        抜粋文。
    """
    rank: int
    filename: str
    score: float
    page: int | None
    snippet: str
    
    
def make_search_results( 
    results: SearchScores, 
    query: QueryWords, 
    resources: SearchResources,
) -> list[SearchResult]:
    """
    検索の結果をリストで作成する。
    
    Parameters
    ----------
    results : searchScores
        検索結果。
    query : QueryWords
        前処理後の検索語。
    resources : SearchResources
        検索に必要なリソース。
    
    Returns
    -------
    list[SearchResult]
        検索結果の一覧をリストにする。
    """
    search_results: list[SearchResult] = []
    rank = 1
    for doc_id, score in results:
        
        if score <= 0:
            continue
        
        highlights = highlight_text(resources.body_texts[doc_id], query)
        if not highlights:
            continue
        
        highlight = select_best_highlight(highlights, query)
        search_result = SearchResult(
            rank=rank,
            filename=resources.pdf_files[doc_id],
            score=score,
            page=highlight.page,
            snippet=highlight.snippet,
        )

        search_results.append(search_result)
        
        rank += 1
        
    return search_results

def display_preprocess_results(
    resources: SearchResources,
):
    """
    ターミナル版の結果の表示をする。
    
    Parameters
    ----------
    resources : SearchResources
        検索に必要なリソース。
    """
    
    print(f"\nHybrid alpha: {resources.hybrid_best_alpha}")
    print(f"Bm25+Vector alpha: {resources.bm25vector_best_alpha}")
    print("===前処理結果===")

    for filename, summary in zip(resources.pdf_files, resources.summary_docs):
        print(f"{filename}")
        print(summary)
        print("-----")
        
def display_query(
    query: QueryWords,
):
    """
    ターミナル用検索語表示をする。
    
    Parameters
    ----------
    query : QueryWords
        前処理後の検索語。
    """
    print("検索語:", " ".join(query))
    
    
def display_title(
    title: str,
):
    """
    ターミナル用タイトル表示。
    
    Parameters
    ----------
    title : str
        検索手法のタイトル。
    """
    print(f"\n==={title}===")
    
    
def display_results(
    result: SearchResult
):
    """
    ターミナル版でプリント表示する。
    
    Parameters
    ----------
    result : SearchResult
        検索結果の情報。
    """
    print(f"{result.rank}位")
    print(f"ファイル: {result.filename}")
    print(f"スコア: {result.score:.4f}")
    page = (
        "該当なし"
        if result.page is None
        else f"{result.page}ページ"
    )
    print(f"ページ: {page}")
    print(f"抜粋: {result.snippet}")
    print("-"*30)