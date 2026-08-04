import math
from collections import Counter
from search_types import (
    PdfFiles,
    SearchScores,
    NormalizedDocs,
)

class BM25:
    def __init__(
        self, 
        docs: list[str | list[str]],
        k1: float = 1.5, 
        b: float = 0.75,
    ):
        """
        BM25による全文検索を行うクラス。
        
        文書集合からBM25の検索インデックスを構築し、
        クエリに対する関連度スコアを計算する。
        
        Parameters
        ----------
        docs : list[str | list[str]]
            検索対象の文書一覧。
        k1 : float
            頻度飽和を調整するパラメータ。
        b : float
            文書長補正の強さを調整するパラメータ。
        """
        self.docs = self._normalize_docs(docs)
        self.N = len(self.docs)
        self.df = self._build_document_frequency()
        self.doc_freqs = self._build_term_frequency()
        self.avgdl = self._compute_average_document_length()
        
        self.k1 = k1
        self.b = b
        
    def _normalize_docs(
        self,
        docs: list[str | list[str]],
    ) ->NormalizedDocs:
        """
        文書の前処理をする。
        
        Parameters
        ----------
        docs : list[str | list[str]]
            検索対象の文書一覧。
        
        Returns
        -------
        list[list[str]]
            前処理された文書。
        """
        normalized_docs = []
        for doc in docs:
            if isinstance(doc, str):
                normalized_docs.append(doc.split())
            else:
                normalized_docs.append(doc)
        return normalized_docs
        
    def _build_document_frequency(self) -> Counter[str]:
        """
        文書頻度を計算する。
        
        Returns
        -------
        Counter[str]
            文書の出現頻度。
        """
        self.df = Counter()
        for doc in self.docs:
            for word in set(doc):
                self.df[word] += 1
        return self.df
                        
    def _build_term_frequency(self) -> list[Counter[str]]:
        """
        各文書の単語頻度を計算する。
        
        Returns
        -------
        list[Counter[str]]
            各文書の単語の頻度。
        """
        doc_freqs: list[Counter[str]] = [
            Counter(doc)
            for doc in self.docs
        ]

        return doc_freqs
            
    def _compute_average_document_length(self) -> float:
        """
        平均文書長を計算する。
        
        Returns
        -------
        float
            平均文書長。
        """
        total_len = sum(
            len(doc) for doc in self.docs
        )
        return total_len / self.N
        
        
    def score(self, query: PdfFiles, doc_index: int) -> float:
        """
        指定した文書に対するBM25スコアを計算する。
        
        Parameters
        ----------
        query : PdfFiles
            前処理後の検索語。
        doc_index : int
            文書のインデックス。
        
        Returns
        -------
        float
            スコア。
        """
        score = 0.0
        doc = self.docs[doc_index]
        doc_len = len(doc)
        freqs = self.doc_freqs[doc_index]
        
        for q in query:
            if q not in freqs:
                continue
            
            df = self.df[q]
            idf = math.log((self.N - df + 0.5) / (df + 0.5) + 1)
            
            tf = freqs[q]
            # BM25のスコアを加算
            score += idf * (tf * (self.k1 + 1)) / (
                tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
            )
        
        return score
    
    def search(self, query: PdfFiles, top_n: int = 5) -> SearchScores:
        """
        BM25検索を実行する。
        
        Parameters
        ----------
        query : PdfFiles
            検索語。
        top_n : int
            返す個数。
        
        Returns
        -------
        SearchScores
            スコア順に並んだ検索結果。
        """
        scores: list[tuple[int, float]] = [
            (i, self.score(query, i))
            for i in range(self.N)
        ]
        
            
        scores.sort(key=lambda result: result[1], reverse=True)
        
        return scores[:top_n]