import re
from highlight_score import score_highlight
from search_types import (
    QueryWords,
    PdfPages,
    HighlightResult,
)

DISPLAY_SYNONYMS = {
    "人工知能": ["AI", "ＡＩ"],
    "生成ai": ["生成 AI", "生成AI"],
    "大規模言語モデル": ["LLM"],
}

EARLY_PAGE_THRESHOLD = 2

    
def make_candidates(query_words: QueryWords) -> QueryWords:
    """
    検索語候補を作成する。
    
    検索語に表示用の類義語を追加し、
    重複を除去して長い順に並べ替える。
    
    Parameters
    ----------
    query_words : QueryWords
        検索語。
    Returns
    -------
    QueryWords
        候補。
    """
    candidates = []
    
    for word in query_words:
        candidates.append(word)
        
        if word in DISPLAY_SYNONYMS:
            candidates.extend(DISPLAY_SYNONYMS[word])
            
            
    candidates = list(dict.fromkeys(candidates))
    candidates.sort(key=len, reverse=True)
    
    return candidates

def highlight_text(
    text: PdfPages, 
    query_words: QueryWords, 
    window: int = 50
) -> list[HighlightResult]:
    """
    ハイライトを作成する。
    
    Parameters
    ----------
    text : PdfPages
        PDFの全文
    query_words : QueryWords
        検索語のリスト。
    window : int
        検索語の前後何文字表示するか。
    
    Returns
    -------
    list[HighlightResult]
        ハイライトの候補リスト。
    """
    # 検索候補作成
    candidates = make_candidates(query_words)
    highlights: list[HighlightResult] = []
    
    # すべてのヒット箇所を収集
    for candidate in candidates:
        for page in text:
            
            matches = re.finditer(
                re.escape(candidate),
                page["text"],
                flags=re.IGNORECASE
            )
            for match in matches:
                
                # ハイライト  
                start = max(0, match.start() - window)
                end = min(len(page["text"]), match.end() + window)
                
                # スニペット作成
                snippet = page["text"][start:end] 
                
                # パターン作成
                pattern = "|".join(
                        re.escape(word)
                        for word in candidates
                    )
                
                # 一回だけ置換
                snippet = re.sub(
                    pattern,
                    lambda m: f"【{m.group()}】",
                    snippet,
                    flags=re.IGNORECASE,
                )
                highlights.append(HighlightResult(
                    page=page["page"],
                    keyword=candidate,
                    snippet=snippet
                ))
    return highlights

def select_best_highlight(
    highlights: list[HighlightResult],
    query_words: QueryWords,
) -> HighlightResult:
    """
    表示するのに適したハイライトを選択する。
    
    Parameters
    ----------
    highlights : list[HighlightResult]
        抽出されたハイライトのリスト
    query_words : QueryWOrds
        検索語のリスト。
        
    Returns
    -------
    HighlightResult
        最も適したハイライト
    """
    if not highlights:
        return HighlightResult(
            page=None,
            keyword="",
            snippet="該当箇所なし"
        )
    content_highlights = [
        highlight
        for highlight in highlights 
        if highlight.page > EARLY_PAGE_THRESHOLD
    ]
            
    if content_highlights:
        return max(
            content_highlights,
            key=lambda h: score_highlight(
                h,
                query_words,
            ),
        )
    return highlights[0]

