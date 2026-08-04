import time
import streamlit as st
from summarizer import extract_keywords
from query_expansion import expand_query
from normalize_text import normalize_text
from pdf_loader import load_uploaded_pdfs
from resources import (
    SearchResources,
    create_search_resources,
)
from search import search_all
from result import make_search_results
from display import (
    show_uploaded_files,
    show_query,
    show_elapsed_time,
    show_search_title,
    show_search_results,
)
from search_types import (
    Query,
    PdfFiles,
    PdfPages,
    test_queries,
)

@st.cache_resource
def get_resources(
    texts: PdfPages,
    pdf_files: PdfFiles,
    test_queries: Query,
) -> SearchResources:
    """
    検索に必要なリソースを作成する。
    
    Parameters
    ----------
    texts : PdfPages
        PDFごとのページデータ。
    pdf_files : list[str]
        PDFファイル名一覧。
    test_queries : Query
        学習用の検索語。
        
    Returns
    -------
    SearchResources
        検索に必要なリソース。
    """
    return create_search_resources(
        texts,
        pdf_files,
        test_queries,
    )

def preprocess_query(query: str) -> PdfFiles:
    """
    検索語を前処理する。
    
    検索語を正規化し、
    キーワード抽出とクエリ拡張を行う。
    
    Parameters
    ----------
    query : str
        検索語。
        
    Returns
    -------
    PdfFiles
        前処理された検索語。
    """
    normalized_query = normalize_text(query)
    keywords = extract_keywords(
        normalized_query, 
        filename=None,
    )
    expanded_query = expand_query(keywords)
    return expanded_query
    
st.title("PDF検索システム")

st.write("検索したいPDFをアップロードしてください")

uploaded_files = st.file_uploader(
    "PDFを選択してください",
    type="pdf",
    accept_multiple_files=True,
)

# PDFがアップロード後の処理
if uploaded_files:
    
    texts, pdf_files = load_uploaded_pdfs(uploaded_files)
    resources = get_resources(
        texts,
        pdf_files,
        test_queries,
    )
    
    show_uploaded_files(pdf_files)
        
    query = st.text_input("検索語を入力してください")
    if st.button("検索"):
        if not query:
            st.warning("検索語を入力してください")
        
        else:
            start = time.perf_counter()
            expanded_query = preprocess_query(query)
            show_query(expanded_query)
            query_words = [
                word for word, _ in expanded_query
            ]
            results = search_all(query_words, resources)
            end = time.perf_counter()
            elapsed = end - start
            show_elapsed_time(elapsed)
            for title, result in results.items():
                hit_count = len(result)
                show_search_title(title, hit_count)
                search_results = make_search_results(
                    result,
                    query_words,
                    resources,
                )
                
                show_search_results(search_results)
                