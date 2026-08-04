import math
from dataclasses import dataclass
from search_types import (
    SearchScores,
    PdfFiles,
    AnswerFiles,
)

DEFAULT_K = 5

@dataclass
class HitResult:
    """
    検索結果のヒット情報。
    
    Parameters
    ----------
    hits : int
        正解文書のヒット数。
    retrieved_files : PdfFiles
        上位k件で取得したファイル一覧。
    """
    hits: int
    retrieved_files: PdfFiles
    
        
def get_retrieved_files(
    results: SearchScores, 
    pdf_files: PdfFiles, 
    k: int,
) -> PdfFiles:
    """
    上位k件の検索結果をファイル名へ変換。
    
    Parameters
    ----------
    results : SearchScores
        検索の結果。
    pdf_files : PdfFiles
        PDFファイル名一覧。
    k : int
        抽出する件数。
    
    Returns
    -------
    AnswerFiles
        k件の検索結果。
    """
    
    return [pdf_files[doc_id] for doc_id, _ in results[:k]]


def count_hits(
    retrieved_files: PdfFiles,
    answer_files: AnswerFiles,
) -> int:
    """
    検索結果と正解ファイルの一致数を数える.
    
    Parameters
    ----------
    retrieved_files : PdfFiles
        検索結果のファイル。
    answer_files : AnswerFiles
        正解ファイル。
    
    Returns
    -------
    int
        検索結果が正解のファイルとどのくらい合っているか。
    """

    return len(
        set(retrieved_files) 
        & 
        set(answer_files)
    )


def get_hits(
    results: SearchScores,
    answer_files: AnswerFiles,
    pdf_files: PdfFiles,
    k: int,
) -> HitResult:
    """
    ヒット件数と取得ファイルをまとめて取得する。
    
    Parameters
    ----------
    results : SearchScores
        検索結果。
    answer_files : AnswerFiles
        正解ファイル。
    pdf_files : PdfFiles
        PDFファイル名一覧。
    k : int
        抽出する検索結果の件数。
        
    Returns
    -------
    HitResult
        ヒット件数と取得したファイル一覧。
    """
    
    if not results:
        return HitResult(
            hits=0,
            retrieved_files=[],
        )
        
    retrieved_files = get_retrieved_files(
        results,
        pdf_files,
        k,
    )
    
    hits = count_hits(
        retrieved_files,
        answer_files,
    )
    
    return HitResult(
        hits=hits, 
        retrieved_files=retrieved_files,
    )


def recall_at_k(
    results: SearchScores,
    answer_files: AnswerFiles,
    pdf_files: PdfFiles,
    k: int = DEFAULT_K,
) -> float:
    """
     正解文書のうち取得できた割合
     
     Parameters
     ----------
     results : SearchScores
        検索結果。
    answer_files : AnswerFiles
        正解ファイル。
    pdf_files : PdfFiles
        PDFファイル名一覧。
    k : int
        抽出する検索結果の件数。
    
    Returns
    -------
    float
        Recall@k。
        正解文書のうち取得できた割合。
    """
    
    if not answer_files:
        return 0.0
    
    hit_result = get_hits(
        results,
        answer_files,
        pdf_files,
        k,
    )
    
    return hit_result.hits / len(answer_files)


def precision_at_k(
    results: SearchScores,
    answer_files: AnswerFiles,
    pdf_files: PdfFiles,
    k: int = DEFAULT_K,
) -> float:
    """
    取得した文書のうち正解だった割合
    
    Parameters
    ----------
    results : SearchScores
        検索の結果。
    answer_files : AnswerFiles
        正解ファイル。
    pdf_files : PdfFiles
        PDFファイル名一覧。
    k : int
        抽出した件数。
        
    Returns
    -------
    float
        Precision@k。
        取得文書のうち正解だった割合。
    """
    
    hit_result = get_hits(
        results,
        answer_files,
        pdf_files,
        k,
    )
    
    if not hit_result.retrieved_files:
        return 0.0

    
    return hit_result.hits / len(hit_result.retrieved_files)


def f1_at_k(
    results: SearchScores,
    answer_files: AnswerFiles,
    pdf_files: PdfFiles,
    k: int = DEFAULT_K,
) -> float:
    """
    再現率と適合率の調和平均。
    
    Parameters
    ----------
    results : SearchScores
        検索の結果。
    answer_files : AnswerFiles
        正解ファイル。
    pdf_files : PdfFiles
        PDFファイル名一覧。
    k : int
        抽出した件数。
    
    Returns
    -------
    float
        recall_at_kとprecision_at_kの調和平均。
    """
    
    recall = recall_at_k(
        results,
        answer_files,
        pdf_files,
        k,
    )
    
    precision = precision_at_k(
        results,
        answer_files,
        pdf_files,
        k,
    )
    
    denominator = recall + precision
    
    if denominator == 0:
        return 0.0
    
    return (
        2 * recall * precision
        /
        (denominator)
    )
    

def mrr_at_k(
    results: SearchScores,
    answer_files: AnswerFiles,
    pdf_files: PdfFiles,
    k: int = DEFAULT_K,
) -> float:
    """
    最初に正解文書が現れた順位を評価
    
    Parameters
    ----------
    results : SearchScores
        検索結果。
    answer_files : AnswerFiles
        正解ファイル。
    pdf_files : PdfFiles
        PDFファイル名一覧。
    k : int
        抽出した件数。
    
    Returns
    -------
    float
        Reciprocal Rank。
        最初の正解文書の順位の逆数。
    """
   
    hit_result = get_hits(
        results,
        answer_files,
        pdf_files,
        k,
    )
    
    for rank, filename in enumerate(
        hit_result.retrieved_files,
        start=1,
    ):
        if filename in answer_files:
            return 1 / rank
    return 0.0


def average_precision_at_k(
    results: SearchScores,
    answer_files: AnswerFiles,
    pdf_files: PdfFiles,
    k: int = DEFAULT_K,
) -> float:
    """
    正解文書が現れる順位ごとのPrecisionの平均
    
    Parameters
    ----------
    results : SearchScores
        検索結果。
    answer_files : AnswerFiles
        正解ファイル。
    pdf_files : PdfFiles
        PDFファイル名一覧。
    k : int
        抽出した件数。
    
    Returns
    -------
    float
        Average Precision。
        正解文書が現れた順位ごとのPrecisionの平均。
    """
    
    if not answer_files:
        return 0.0
    
    hit_result = get_hits(
        results,
        answer_files,
        pdf_files,
        k,
    )
    
    num_hits = 0
    precision_sum = 0
   
    for rank, filename in enumerate(hit_result.retrieved_files, start=1):
        if filename in answer_files:
            num_hits += 1
            precision_sum += num_hits / rank
        
    return precision_sum / len(answer_files)


def calculate_dcg(relevances: list[int]) -> float:
    """
    DCG(Discounted Cumulative Gain)を計算する。
    
    順位が高い正解ほど大きなスコアとなる。
    
    Parameters
    ----------
    relevances : list[int]
        正解したファイル。
    
    Returns
    -------
    float
        Discounted Cumulative Gain。
        上位に正解文書があるほど高い値となる。
    """
    
    dcg = 0.0
    
    for rank, relevance in enumerate(
        relevances,
        start=1,
    ):
        dcg += relevance / math.log2(rank + 1)
        
    return dcg


def ndcg_at_k(
    results: SearchScores,
    answer_files: AnswerFiles,
    pdf_files: PdfFiles,
    k: int = DEFAULT_K,
) -> float:
    """
    理想順位との一致度を評価する。
    正解文書が上位にあるほど高い値となる。

    Parameters
    ----------
    results : SearchScores
        検索結果。
    answer_files : AnswerFiles
        正解ファイル。
    pdf_files : PdfFiles
        PDFファイル名一覧。
    k : int
        抽出した件数。
    
    Returns
    -------
    float
        Normalized Discounted Cumulative Gain。
        正解文書が理想順位に近いほど1に近づく。
    """
    
    if not answer_files:
        return 0.0
    
    hit_result = get_hits(
        results,
        answer_files,
        pdf_files,
        k,
    )
    
    relevances = [
        1 if filename in answer_files else 0
        for filename in hit_result.retrieved_files
    ]
    
    # 理想順位で正解となる文書数
    ideal_hits = min(len(answer_files), k)
    ideal_relevances = [1] * ideal_hits
    
    # 実際の検索結果のDCG
    dcg = calculate_dcg(relevances)
   
    # 理想順位のDCG
    idcg = calculate_dcg(ideal_relevances)
   
    if idcg == 0:
        return 0.0
    
    return dcg / idcg


# 評価関数と表示名の対応
METRIC_NAMES = {
        recall_at_k: "Recall",
        precision_at_k: "Precision",
        f1_at_k: "F1",
        mrr_at_k: "MRR",
        average_precision_at_k: "AP",
        ndcg_at_k: "NDCG",
    }
