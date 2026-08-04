import unicodedata
import re
from normalization_rules import NORMALIZE_DICT
from synonyms import SYNONYMS

def replace_text(text: str) -> str:
    """
    受け取ったPDFの同義語の置き換え。
    
    Parameters
    ----------
    text : str
        入力文字列。
    
    Returns
    -------
    str
        同義語を置き換えたPDF文。
    """
    for before, after in SYNONYMS.items():
        text = text.replace(
            before,
            after,
        )
    return text

def normalize_text(text: str) -> str:
    """
    NFKCを用いて書式などを統一し、
    全文を処理しやすい形に変換する。
    
    Parameters
    ----------
    text : str
        PDF全文。
    
    Returns
    -------
    str
        正規化されたPDF全文。
    """
    
    text = unicodedata.normalize("NFKC", text)
    
    text = text.lower()

    for before, after in NORMALIZE_DICT.items():
        text = text.replace(
            before.lower(),
            after.lower(),
        )
        
    text = replace_text(text)
   
    text = re.sub(r"\s+", " ", text).strip()
   
    text = re.sub(r"[^\w\s]", "", text)          
    
    return text

