import streamlit as st
from result import SearchResult
from search_types import (
    PdfFiles,
    ExpandedQuery,
)

def show_uploaded_files(pdf_files: PdfFiles):
    """
    アップロードしたPDFを表示する。
    
    Parameters
    ----------
    pdf_files : PdfFiles
        アップロードされたPDFファイル名一覧。
    """
    st.subheader(" 📄 アップロードしたPDF")
    
    for pdf in pdf_files:
        st.write(f"### 📄 - {pdf}")
        
        
def show_query(expanded_query: ExpandedQuery):
    """
    前処理後の検索語を表示する。
    
    Parameters
    -----------
    expanded_query : ExpandedQuery
        前処理された検索語。
    """
    st.write("検索語:", " ".join(
        word 
        for word, score in expanded_query
        )
    )
    
    
def show_elapsed_time(elapsed : float):
    """
    検索時間を表示する。
    
    Parameters
    ----------
    elapsed : float
        検索にかかった時間 （秒）。
    """
    st.write(f"### ⌛ 検索時間: {elapsed:.3f} 秒")
    
    
def show_search_title(title: str, hit_count: int):
    """
    評価指標とヒット件数を表示する。
    
    Parameters
    ----------
    title : str
        評価指標名。
    hit_count : int
        ヒット件数。
    """
    st.subheader(f"{title} ({hit_count}件)")


def show_search_results(search_results: list[SearchResult]):
    """
    検索結果を表示する。
    
    Parameters
    ----------
    search_results : list[SearchResult]
        表示する検索結果一覧。
    """
    for search_result in search_results:
        with st.expander(f"📄 {search_result.rank}位 | {search_result.filename}"):
            col1, col2 = st.columns([2, 1])
            page = (
                "該当なし"
                if search_result.page is None
                else f"{search_result.page}ページ"
            )
            with col1:
                st.markdown(f"### 📖 **ページ**: {page}")
            with col2:
                st.markdown(f"### ⭐ **スコア**: {search_result.score:.4f}")
            st.markdown(f"### 💬 **抜粋**: {search_result.snippet}")