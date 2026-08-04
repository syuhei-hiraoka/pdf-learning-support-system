from search_types import EvaluationResults

def print_evaluation_results(
    results: EvaluationResults,
    k: int,
):
    """
    それぞれの検索手法のスコア表示。
    
    Parameters
    ----------
    results : EvaluationResults
        検索結果。
    k : int
        抽出した件数。
    """
    
    for metric_name, scores in results.items():
        print(f"\n==={metric_name}@{k}===")
        
        for method_name, score in scores.items():
            print(f"{method_name}: {score:.3f}")