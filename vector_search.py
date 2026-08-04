from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from search_types import (
    PdfFiles,
    QueryWords,
    SearchScores,
)

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

class VectorSearch:
    
    
    def __init__(self, docs: PdfFiles):
        """
        SentenceTransformerを用いた
        ベクトル検索を行うクラス。
        
        Parameters
        ----------
        docs : PdfFiles
            PDFの全文。
        """
        self.model = SentenceTransformer(MODEL_NAME)
        
        self.doc_vectors = self.model.encode(docs)
        
        
    def search(self, query: QueryWords) -> SearchScores:
        """
        クエリと各文書のベクトル類似度を計算し、
        スコア順に検索結果を返す。
        
        Parameters
        ----------
        query : QueryWords
            前処理後の検索語。
        
        Returns
        -------
        SearchScores
            ベクトル検索の結果。
        """
        query_vector = self.model.encode(
            " ".join(query)
        )
        
        scores = cosine_similarity(
            [query_vector],
            self.doc_vectors
        )[0]
        
        results = sorted(
            enumerate(scores),
            key=lambda result: result[1],
            reverse=True
        )
        
        return results