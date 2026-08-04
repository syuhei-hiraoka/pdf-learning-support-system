from dataclasses import dataclass
from collections.abc import Callable


SearchScores = list[tuple[int, float]]
SearchResults = dict[str, SearchScores]
QueryWords = list[str]
ExpandedQuery = list[tuple[str, float]]

SearchDocs = list[list[str]]
NormalizedDocs = list[list[str]]
PageData = dict
PdfPages = list[PageData]
PdfData = tuple[list[PdfPages], list[str]]
PdfFiles = list[str]
AnswerFiles = list[str]
ListScores = list[float]
JudgeScores = list[int]

PageData = dict[str, int | str]
PdfTexts = list[list[PageData]]
KeywordDocs = list[list[str]]
JoinedDocs = list[str]

SearchFunction = Callable[[QueryWords], SearchScores]
MetricFunction = Callable[
    [SearchScores, AnswerFiles, PdfFiles, int], 
    float
]

SearchMethods = dict[str, SearchFunction]
EvaluationResults = dict[str, dict[str, float]]

TFIDFSearch = Callable[
    [list[str], str], 
    list[tuple[int, float]]
]

BM25_TITLE = "BM25検索結果"
TFIDF_TITLE = "TF-IDF検索結果"
HYBRID_TITLE = "Hybrid検索結果"
VECTOR_TITLE = "ベクトル検索結果"
RRF_TITLE = "RRF検索結果"
BM25_VECTOR_HYBRID_TITLE = "BM25+Vector検索結果"
LTR_TITLE = "LTR学習"

@dataclass
class HighlightResult:
    """
    ハイライトオブジェクトを作成。
    
    Parameters
    ----------
    page : int | None
        PDFのページ。
    keyword : str
        キーワード。
    snippet : str
        抽出文。
    """
    page: int | None
    keyword: str
    snippet: str
    
@dataclass
class Feature:
    doc_id: int
    doc_name: str
    bm25_score: float
    tfidf_score: float
    vector_score: float
    rrf_score: float
    bm25_vector_score: float
    keyword_count: int
    key_density: float
    doc_length: float
    title_match: float
    label: int | None = None
    
    
@dataclass
class Query:
    """
    検索クエリと正解文書を表すデータクラス。
    
    Parameters
    ----------
    words : list[str]
        検索語。
    answers : list[str]
        正解となるPDFファイル名。
    """
    
    words: list[str]
    answers: list[str]
    
    
test_queries = [        
    Query(
        # 完全一致
        words=["独立行政法人"], 
        answers=["sample.pdf"],
    ),
    Query(
        words=["随意契約"], 
        answers=["sample.pdf"],
    ),
    Query(
        words=["企画競争"], 
        answers=["sample.pdf"],
    ),
    Query(
        words=["再就職"],
        answers=["sample.pdf"],
    ),
    Query(
        words=["役員経験者"],
        answers=["sample.pdf"],
    ),
    Query(
        words=["著作権"],
        answers=["ai_guideline.pdf"],
    ),
    Query(
        words=["個人情報"],
        answers=["ai_guideline.pdf"],
    ),
    Query(
        words=["禁止事項"],
        answers=["ai_guideline.pdf"],
    ),
    Query(
        words=["教育情報課"],
        answers=["ai_guideline.pdf"],
    ),
    Query(
        words=["成績評価"],
        answers=["ai_guideline.pdf"],
    ),
    Query(
        words=["ディープラーニング"],
        answers=["G検定紹介資料_202606.pdf"],
    ),
    Query(
        words=["エコシステム"],
        answers=["G検定紹介資料_202606.pdf"],
    ),
    Query(
        words=["JDLA"],
        answers=["G検定紹介資料_202606.pdf"],
    ),
    Query(
        words=["AI人材"],
        answers=["G検定紹介資料_202606.pdf"],
    ),
    Query(
        words=["活用リテラシー"],
        answers=["G検定紹介資料_202606.pdf"],
    ),
    Query(
        words=["AI倫理"],
        answers=["G検定紹介資料_202606.pdf"],
    ),
    Query(
        words=["生成AI"],
        answers=["G検定紹介資料_202606.pdf"],
    ),    
    Query(
        words=["機械学習"],
        answers=["machine_learning.pdf"],
    ),
    Query(
        words=["データ分析"],
        answers=["machine_learning.pdf"],
    ),
    Query(
        words=["正則化"],
        answers=["machine_learning.pdf"],
    ),
    Query(
        words=["経験","学習"],
        answers=["machine_learning.pdf"],
    ),
    Query(
        words=["訓練データ"],
        answers=["machine_learning.pdf"],
    ),
    Query(
        words=["強化学習"],
        answers=["machine_learning.pdf"],
    ),
    Query(
        words=["回帰"],
        answers=["machine_learning.pdf"],
    ),
    Query(
        words=["分類"],
        answers=["machine_learning.pdf"],
    ),
    Query(
        words=["損失関数"],
        answers=["machine_learning.pdf"],
    ),
    Query(
        words=["行政法人"],
        answers=["sample.pdf"],
    ),
    Query(
        words=["再就職", "採用"],
        answers=["sample.pdf"],
    ),
    Query(
        words=["公表日"],
        answers=["sample.pdf"],
    ),
    Query(
        words=["AI", "ルール"],
        answers=["ai_guideline.pdf"],
    ),
    Query(
        words=["AI", "利用"],
        answers=["ai_guideline.pdf"],
    ),
    Query(
        words=["学生", "AI"],
        answers=["ai_guideline.pdf"],
    ),
    Query(
        words=["AI", "禁止"],
        answers=["ai_guideline.pdf"],
    ),
    Query(
        words=["盗作"],
        answers=["ai_guideline.pdf"],
    ),
    Query(
        words=["カテゴリ値"],
        answers=["machine_learning.pdf"],
    ),
    Query(
        words=["離散値"],
        answers=["machine_learning.pdf"],
    ),
    Query(
        words=["学生作品"],
        answers=["ai_guideline.pdf"],
    ),
    Query(
        words=["レポート"],
        answers=["ai_guideline.pdf"],
    ),
    Query(
        words=["Chat-GPT"],
        answers=["G検定紹介資料_202606.pdf"],
    ),
    Query(
        words=["ChatGPT"],
        answers=["G検定紹介資料_202606.pdf"],
    ),
    Query(
        words=["元職員"],
        answers=["sample.pdf"],
    ),
    Query(
        words=["sepal.length", "がく弁の長さ"],
        answers=["machine_learning.pdf"],
    ),
    Query(
        words=["生成AI", "ChatGPT"], 
        answers=["ai_guideline.pdf", "G検定紹介資料_202606.pdf"],
    ),
    Query(
        words=["契約方式"],
        answers=["sample.pdf"],
    ),
    Query(
        words=["教材", "業務文書"],
        answers=["ai_guideline.pdf"],
    ),
    Query(
        words=["役員", "再就職"],
        answers=["sample.pdf"],
    ),
    Query(
        words=["ガイドライン"],
        answers=["G検定紹介資料_202606.pdf", "ai_guideline.pdf"],
    ),
    Query(
        words=["ChatGPT"],
        answers=["ai_guideline.pdf", "G検定紹介資料_202606.pdf"],
    ),
    Query(
        words=["情報"],
        answers=["sample.pdf", "ai_guideline.pdf", 
                    "G検定紹介資料_202606.pdf", "machine_learning.pdf"],
    ),
]