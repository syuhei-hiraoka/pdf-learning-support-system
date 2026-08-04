from search_types import (
    QueryWords,
    ExpandedQuery,
)

QUERY_EXPANSION = {
    "人工知能": [
        ("深層学習",0.5),
        ("機械学習",0.7),
        ("生成ai",0.9),
    ],

    "大規模言語モデル": [
        ("transformer",0.6),
        ("生成ai",0.8),
    ],

    "pdf": [
        ("文書",0.6),
        ("ファイル",0.9),
    ],
}

def remove_duplicates(words: list[tuple[str, float]]) -> list[tuple[str, float]]:
    """
    検索語の重複を削除する。
    
    元の順序を維持したまま重複を取り除く。
    
    Parameters
    ----------
    words : list[tuple[str, float]]
        検索語のリスト。
    
    Returns
    -------
    list[tuple[str, float]]
        元の順序を維持したまま重複を除去したリスト。
    """
    
    weights = {}
    for word, weight in words:
        if word not in weights:
            weights[word] = weight
        else:
            if weights[word] < weight:
                weights[word] = weight
            else:
                continue
                
    return list(weights.items())


def expand_query(query: QueryWords) -> ExpandedQuery:
    """
    検索語を拡張する。
    
    QUERY_EXPANSIONに登録された関連語を追加し、
    重複を除去した検索語のリストを返す。
    
    Parameters
    ----------
    query : QueryWords
        検索語。
    
    Returns
    -------
    list[tuple[str, float]]
        関連語を追加し、重複を除去した検索語のリスト。
    """
    
    expanded = []
    
    for word in query:
        weighted_word = (word, 1.0)
        
        expanded.append(weighted_word)
        
        if word in QUERY_EXPANSION:
            for expand_word, weight in QUERY_EXPANSION[word]:
                expanded.append(
                    (expand_word, weight)
                )

    return remove_duplicates(expanded)

def get_query_words(
    expanded_query: ExpandedQuery,
) -> QueryWords:
    """
    拡張された検索語から検索語のリストを取得する。
    
    Parameters
    ----------
    expanded_query : ExpandedQuery
        拡張された検索語。
    
    Returns
    -------
    QueryWords
        検索語のリスト。
    """
    
    return [word for word, _ in expanded_query]