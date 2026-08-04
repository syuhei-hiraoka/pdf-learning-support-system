from janome.tokenizer import Tokenizer as JanomeTokenizer
from collections import Counter
from stop_words import (
    COMMON_STOP_WORDS, 
    PDF_STOP_WORDS,
)
from normalize_text import normalize_text
from search_types import QueryWords

VALID_NOUNS = {
    "一般", 
    "固有名詞", 
    "サ変接続"
}

STOP_SINGLE_WORDS = {
        "日", "年", "月", "人", "者", "等",
        "場合", "情報", "状況", "対象"
    }

START_WORD = 2
END_WORD = 20

def extract_keywords(
    text: str, 
    filename: str =None, 
    top_n: int =None
) -> QueryWords:
    """
    PDFファイルから不要な単語を除去し、
    扱いやすい形に前処理する。
    
    Parameters
    ----------
    text : str
        PDFの全文。
    filename : str | None
        PDFファイル名の一覧。
    top_n : int | None
        上位のデータを抽出。
    
    Returns
    -------
    QueryWords
        不要な文字列を除去した単語リスト。
    """
    text =normalize_text(text)
    TOKENIZER = JanomeTokenizer()
    words = []
    compound_word = ""
    
    
    for token in TOKENIZER.tokenize(text):
        
        pos_info = token.part_of_speech.split(",")
        
        pos = pos_info[0]
        sub_pos = pos_info[1]
        
        word = token.surface
        
        valid = (
            (pos=="名詞"
            and sub_pos in VALID_NOUNS
            )
            or pos=="接頭詞"
        )
        if word in STOP_SINGLE_WORDS:
            valid = False
            
        if valid:
            compound_word += word

        else:
            if START_WORD <= len(compound_word) <= END_WORD:
                words.append(compound_word)

            compound_word = ""
    if START_WORD <= len(compound_word) <= END_WORD:
        words.append(compound_word)
            
    stop_words = set(COMMON_STOP_WORDS)
    if filename in PDF_STOP_WORDS:
        stop_words.update(
            PDF_STOP_WORDS[filename]
      )
        
    filtered_words = [
        w
        for w in words
        if w not in stop_words
    ]
    
    counts = Counter(filtered_words)
    
    if top_n is not None:
        return [word for word, _ in counts.most_common(top_n)]
    
    return [word for word, _ in counts.most_common()]