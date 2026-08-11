from dataclasses import dataclass
from tfidf import run_tfidf
from BM25_files import BM25
from hybrid_search import HybridSearch
from vector_search import VectorSearch
from rrf_search import RRFSearch
from bm25_vector_hybrid import BM25VectorHybrid
from preprocess import (
    make_keyword_docs,
    remove_table_of_contents,
    make_bm25_docs,
)
from optimizer import optimizer_alpha
from test_queries import test_queries
from learning_to_rank import LearningToRank
from search_types import (
    Query,
    PdfFiles,
    KeywordDocs,
    JoinedDocs,
    PdfTexts,
)
from train_ltr import train_ltr
from pdf_loader import pages_to_text


@dataclass
class SearchResources:
    """
    検索システムで共有するリソースを保持する。
    
    Parameters
    ----------
    bm25 : BM25
        BM25検索器。
    search_engine : HybridSearch
        Hybrid検索器。
    vector : VectorSearch
        ベクトル検索器。
    rrf : RRFSearch
        複数の検索結果を統合した検索器。
    bm25_vector_hybrid : BM25VectorHybrid
        BM25検索とベクトル検索を統合した検索器。
    summary_docs : KeywordDocs
        BM25・Hybrid検索で使用するキーワード文書。
    joined_docs : JoinedDocs
        ベクトル検索用に結合した文書。
    hybrid_best_alpha : float
        BM25とTF-IDFを統合するHybrid検索の最適な重み。
    bm25vector_best_alpha : float
        BM25とベクトル検索を統合する最適な重み。
    texts : PdfTexts
        PDF全文。
    body_texts : PdfTexts
        目次を除いたPDF全文。
    pdf_files : PdfFiles
        PDFファイル名一覧。
    ltr : LearningToRank
        ltr学習。
    """
    bm25: BM25
    search_engine: HybridSearch
    vector: VectorSearch
    rrf: RRFSearch
    bm25_vector_hybrid: BM25VectorHybrid
    summary_docs: KeywordDocs
    joined_docs: JoinedDocs
    hybrid_best_alpha: float
    bm25vector_best_alpha: float
    texts: PdfTexts
    body_texts: PdfTexts
    pdf_files: PdfFiles
    ltr: LearningToRank | None = None
    
def create_search_resources(
    texts: PdfTexts,
    pdf_files: PdfFiles,
    train_queries: list[Query],
) -> SearchResources:
    """
    検索に必要なリソースの作成。
    
    Parameters
    ----------
    texts : PdfTexts
        PDF全文。
    pdf_files : PdfFiles
        PDFファイル名一覧。
    
    Returns
    -------
    SearchResources
        検索リソース。
    """
    
    body_texts = remove_table_of_contents(texts)
    summary_docs = make_keyword_docs(body_texts, pdf_files)
    
    bm25_docs = make_bm25_docs(body_texts)
    bm25 = BM25(bm25_docs)

    joined_docs = [
        pages_to_text(pages)
        for pages in body_texts
    ]
    hybrid = HybridSearch(
        bm25, run_tfidf, summary_docs
    )

    hybrid_best_alpha = optimizer_alpha(
        hybrid,
        test_queries,
        pdf_files
    )

    vector = VectorSearch(joined_docs)

    rrf = RRFSearch()
    
    bm25_vector_hybrid = BM25VectorHybrid(
        bm25,
        vector,
        summary_docs,
    )
    
    bm25vector_best_alpha = optimizer_alpha(
        bm25_vector_hybrid,
        test_queries,
        pdf_files
    )
    
    resources = SearchResources(
        bm25=bm25,
        search_engine=hybrid,
        vector=vector,
        rrf=rrf,
        bm25_vector_hybrid=bm25_vector_hybrid,
        summary_docs=summary_docs,
        joined_docs=joined_docs,
        hybrid_best_alpha=hybrid_best_alpha,
        bm25vector_best_alpha=bm25vector_best_alpha,
        texts=texts,
        body_texts=body_texts,
        pdf_files=pdf_files,
    )
    
    ltr = train_ltr(train_queries, resources)
    
    resources.ltr = ltr
    
    return resources