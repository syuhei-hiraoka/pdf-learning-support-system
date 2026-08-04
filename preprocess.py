from summarizer import extract_keywords
from pdf_loader import pages_to_text
from search_types import(
    PdfPages,
    PdfFiles,
    PdfTexts,
    SearchDocs,
    QueryWords,
)
from document_utils import is_table_of_contents
from janome.tokenizer import Tokenizer

tokenizer = Tokenizer()

def make_keyword_docs(
    texts: list[PdfPages], 
    pdf_files: PdfFiles,
) -> SearchDocs:
    """
    各PDFから検索用キーワードを抽出する
    
    Parameters
    ----------
    texts : list[PdfPages]
        PDF全文のリスト
    pdf_files : PdfFiles
        PDFファイル名のリスト
        
    Returns
    -------
    SearchDocs
        PDFごとの検索キーワード
    """
    
    docs: SearchDocs = []
    
    for pages, filename in zip(texts, pdf_files):
        
        
        docs.append(
            extract_keywords(
                pages_to_text(pages),
                filename,
                top_n=30,
            )
        )
        
    return docs
    
def make_text_docs(
    keyword_docs: SearchDocs,
) -> QueryWords:
    """
    キーワードリストをTF-IDF用の文字列に変換する
    
    Parameters
    ----------
    keyword_docs : SearchDocs
        PDFごとのキーワードリスト
    
    Returns
    -------
    QueryWords
        TF-IDF用に結合した文字列のリスト
    """
    
    return [
        " ".join(doc) 
        for doc in keyword_docs
    ]
    
def remove_table_of_contents(
    texts: PdfTexts,
) -> PdfTexts:
    """
    目次・索引ページを削除する。
    
    Parameters
    ----------
    texts : PdfTexts
        PDF全文
    
    Returns
    -------
    PdfTexts
        目次・索引ページを削除したPDF全文
    """
    
    return [
        [
            page
            for page in pages
            if not is_table_of_contents(
                page["text"]
            )
        ]
        for pages in texts
    ]
    
def make_bm25_docs(
    texts: PdfTexts,
) -> list[list[str]]:
    """
    BM25用の文書を作成する。
    
    Parameters
    ----------
    texts : PdfTexts
        PDF全文
    
    Returns
    -------
    list[list[str]]
        BM25用の文書
    """
    
    docs: list[list[str]] = []
    
    for pages in texts:
        text = pages_to_text(pages)
        tokens = [
            token.surface
            for token in tokenizer.tokenize(text)
        ]
        docs.append(tokens)
    
    return docs