from search_types import (
    SearchScores,
    SearchResults,
)
RRF_K = 60

class RRFSearch:
    
    def search(
        self,
        results: SearchResults
    )  -> SearchScores:
        """
        Reciprocal Rank Fusion。
        複数の異なる検索結果の順位を組み合わせて、
        一つの順位にまとめる。
        
        Parameters
        ----------
        results : SearchResults
            検索結果。
            
        Returns
        -------
        SearchScores
            複数の検索結果を統合した順位。
        """
        
        rrf_scores = {}
        for result in results.values():
            for rank, (doc_id, _) in enumerate(result, start=1):
                if doc_id not in rrf_scores:
                    rrf_scores[doc_id] = 0
                rrf_scores[doc_id] += 1 / (RRF_K + rank)
                
        results = sorted(
            rrf_scores.items(),
            key=lambda result: result[1],
            reverse=True
        )
        
        return results