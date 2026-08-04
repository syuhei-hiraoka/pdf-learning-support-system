import unicodedata
import re

TABLE_WORDS = [
    "目次", "索引", "概要","contents", "chapter", "index", "目次ページ", "索引ページ",
    "目次のページ", "索引のページ", "目次の内容",
]

def is_table_of_contents(
    text: str,
) -> bool:
    """
    目次・索引ページかどうかを判定する。
    
    Parameters
    ----------
    text : str
        ページのテキスト。
    
    Returns
    -------
    bool
        目次・索引ページであればTrue、そうでなければFalse。
    """
    
    text = unicodedata.normalize("NFKC", text)
    
    lower_text = text.lower()
    
    if any(word.lower() in lower_text for word in TABLE_WORDS):
        
        return True
    
    numbers = re.findall(
        r"\d+\s*$",
        text,
        flags=re.MULTILINE
        )
    
    if len(numbers) > 10:
        return True
    
    return False