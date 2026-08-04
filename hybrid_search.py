from BM25_files import BM25
from search_types import (
    TFIDFSearch,
    SearchDocs,
    QueryWords,
    SearchScores,
)


DEFAULT_ALPHA = 0.6

class HybridSearch:
    
    def __init__(
        self, 
        bm25: BM25, 
        tfidf_func: TFIDFSearch,    
        docs: SearchDocs,
    ):
        """
        BM25とTF-IDFを組み合わせた検索手法。
        
        Parameters
        ----------
        bm25 : BM25
            BM25検索器。
        tfidf_func : TFIDFSearch 
            TF-IDF検索を実行する関数。
        docs : SearchDocs
            検索対象の文書一覧。
        """
        self.bm25 = bm25
        self.tfidf_func = tfidf_func
        self.doc_count = len(docs)
        # TF-IDF用に文字列へ変換
        self.tfidf_docs = [
            " ".join(doc) for doc in docs
        ]
        
        
    def search(
        self, 
        query: QueryWords, 
        alpha: float = DEFAULT_ALPHA
    ) -> SearchScores:
        """
        BM25とTF-IDFのそれぞれのスコアを計算し合計する。
        
        Parameters
        ----------
        query : list[str]
            前処理後の検索語。
        alpha : float
            調整率。
        
        Returns
        -------
        SearchScores
            スコア順に並んだ検索結果。
        """
        tfidf_query = " ".join(query)
        
        bm25_scores = dict(
            self.bm25.search(query)
        )
    
        tfidf_scores = dict(
            self.tfidf_func(
                self.tfidf_docs,
                tfidf_query
            )
        )
        
        scores: SearchScores = []
        
        for doc_id in range(self.doc_count):
            
            bm25_score = bm25_scores.get(doc_id, 0)
            tfidf_score = tfidf_scores.get(doc_id, 0)
            
            scores.append(
                (doc_id, 
                 alpha * bm25_score
                 + (1 - alpha) * tfidf_score
                 )
            )
            
        results = sorted(
            scores,
            key=lambda result: result[1],
            reverse=True
        )
        return results