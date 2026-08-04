from BM25_files import BM25
from vector_search import VectorSearch
from search_types import (
    PdfFiles,
    SearchScores,
    SearchDocs,
)

DEFAULT_ALPHA = 0.6

class BM25VectorHybrid:
    def __init__(
        self,
        bm25: BM25,
        vector_search: VectorSearch,
        docs: SearchDocs,
    ):
        """
        BM25検索器とベクトル検索器の検索結果を統合させた検索器。
        
        Parameters
        ----------
        bm25 : BM25
            BM25検索器。
        vector_search : VectorSearch
            ベクトル検索器。
        docs : SearchDocs
            検索対象の文書。
        """
        
        self.bm25 = bm25
        self.vector_search = vector_search
        self.doc_count = len(docs)
    
    def search(
        self,
        query: PdfFiles,
        alpha: float = DEFAULT_ALPHA,
    ) -> SearchScores:
        """
        query : PdfFiles
            前処理後の検索語。
        alpha : float
            調整率。
        
        Returns
        -------
        SearchScores
            BM25検索器とベクトル検索器を統合した検索結果。
        """
        
        bm25_scores = dict(
            self.bm25.search(query)
        )
        
        vector_scores = dict(
            self.vector_search.search(query)
        )
        
        scores: list[tuple[int, float]] = []
        
        for doc_id in range(self.doc_count):
            bm25_score = bm25_scores.get(doc_id, 0)
            vector_score = vector_scores.get(doc_id, 0)
            
            scores.append(
                (doc_id,
                alpha * bm25_score
                + (1 - alpha) * vector_score
                )
            )
        results = sorted(
            scores,
            key=lambda result: result[1],
            reverse=True
        )
            
        return results