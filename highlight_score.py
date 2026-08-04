from search_types import (
    QueryWords,
    HighlightResult,
)
from document_utils import TABLE_WORDS

SHORT_SNIPPET_LENGTH = 30
EARLY_PAGE_THRESHOLD = 2
KEYWORD_HITS_ADD_BONUS = 3

TABLE_OF_CONTENTS_PENALTY = 100
SHORT_SNIPPET_PENALTY = 20
PAGE_PENALTY = 30
EXPLANATION_BONUS = 20
KEYWORD_BONUS = 30
ADD_BONUS = 50

EXPLANATION_WORDS = [
    "とは", "である", "という",
    "用いる", "利用する", 
]

def score_highlight(
    highlight: HighlightResult,
    query_words: QueryWords
) -> int:
    """
    ハイライトにスコアをつける。
    
    Parameters
    ----------
    highlight : HighlightResult
        ハイライト。
    query_words : QueryWords
        検索語。
    
    Returns
    -------
    int
        スコア。
    """
    # 基本点　（スニペット長）
    score = len(highlight.snippet)
    # 目次・索引は大きく減点
    if any(
        word in highlight.snippet
        for word in TABLE_WORDS
    ):
        score -= TABLE_OF_CONTENTS_PENALTY
    # 短いスニペットは減点
    if len(highlight.snippet) < SHORT_SNIPPET_LENGTH:
        score -= SHORT_SNIPPET_PENALTY
    # 本文ページを優先
    if highlight.page is not None and highlight.page <= EARLY_PAGE_THRESHOLD:
        score -= PAGE_PENALTY
    # 説明文らしい文章は加点
    if any(
        word in highlight.snippet
        for word in EXPLANATION_WORDS
    ):
        score += EXPLANATION_BONUS
    # キーワードの出現回数で加点
    keyword_hits = sum(
        highlight.snippet.count(word)
        for word in query_words
    )
    
    if keyword_hits >= KEYWORD_HITS_ADD_BONUS:
        score += ADD_BONUS
    
    score += keyword_hits * KEYWORD_BONUS
    return score