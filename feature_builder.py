from search_types import (
    QueryWords,
    PdfFiles,
    ListScores,
    JudgeScores,
    AnswerFiles,
    Feature,
    BM25_TITLE,
    TFIDF_TITLE,
    VECTOR_TITLE,
    RRF_TITLE,
)
from  pdf_loader import pages_to_text
import math

class FeatureBuilder:
    
    
    def build(
        self,
        query: QueryWords,
        ltr_inputs: dict[int, dict[str, float]],
        body_texts: list[list[str]],
        pdf_files: PdfFiles,
        ) -> list[Feature]:
        """
        LTR学習に必要なリソースを作る。
        
        Parameters
        ----------
        ltr_inputs : dict[int, dict[str, float]]
            ltrの入力。
        pdf_files : PdfFiles
            PDFの文書一覧。
        body_texts : list[list[str]]
            PDFの本文一覧。
        rrf_inputs : dict[int, float]
            RRFの入力。
        
        Returns
        -------
        list[Feature]
            作成したリソースをリストにする。
        """
        
        features: list[Feature] =[]
        
        
        for doc_id, scores in ltr_inputs.items():
            doc_name = pdf_files[doc_id]
            doc_text = body_texts[doc_id]
            title_match = calculate_title_match(query, doc_name)
            document = pages_to_text(doc_text)
            keyword_count = keyword_match_count(
                document,
                query,
            )
            
            feature = Feature(
                doc_id=doc_id,
                doc_name=doc_name,
                bm25_score=scores[BM25_TITLE],
                tfidf_score=scores[TFIDF_TITLE],
                vector_score=scores[VECTOR_TITLE],
                rrf_score=scores[RRF_TITLE],
                bm25_vector_score=scores[BM25_TITLE] + scores[VECTOR_TITLE],
                keyword_count=keyword_count,
                key_density=keyword_count / len(document) if document else 0.0,
                doc_length=len(document),
                title_match=title_match,
                label=None,
            )
            features.append(feature)
    
        return features
    
    def make_X(
        self,
        features: list[Feature],
    ) -> list[ListScores]:
        """
        検索器の検索スコアをリストに追加する。
        
        Parameters
        ----------
        features : list[Feature]
            LTR学習のためのリソース。
            
        Returns
        -------
        list[ListScores]
            検索器の検索スコアをリストにする。
        """
        
        X: list[ListScores] = []
        for feature in features:
            X.append(
                [
                    feature.bm25_score,
                    feature.tfidf_score,
                    feature.vector_score,
                    feature.rrf_score,
                    feature.bm25_vector_score,
                    feature.keyword_count,
                    feature.key_density,
                    math.log1p(feature.doc_length),
                    feature.title_match,
                ]
            )
        return X
    
    def make_y(
        self,
        features: list[Feature],
    ) -> JudgeScores:
        """
        判定ラベルの作成をする。
        
        Parameters
        ----------
        features : list[Feature]
            LTR学習のためのリソース。
        
        Returns
        -------
        JudgeScore
            判定ラベルを追加してリストにする。
        """
        
        y: JudgeScores = []
        
        for feature in features:
            if feature.label is None:
                        raise ValueError("Label has not been assigned.")
                    
            y.append(feature.label)
            
        return y
    
    def to_dataset(
        self,
        features: list[Feature],
    ) -> tuple[ListScores, JudgeScores]:
        """
        LTR学習用データセットを作成する。
        
        Parameters
        ----------
        features : list[Feature]
            LTR学習のためのリソース。
        
        Returns
        -------
        tuple[ListScores, JudgeScores]
            LTR学習用データ。
        """
        
        return (
            self.make_X(features), 
            self.make_y(features),
            )
    
    def add_labels(
        self,
        features: list[Feature],
        answers: list[str],
    ):
        """
        LTR学習用データセットに判定ラベルを追加する。
        
        Parameters
        ----------
        features : list[Feature]
            LTR学習のためのリソース。
        answers : list[str]
            正解文書のリスト。
        Returns
        -------
        list[Feature]
            判定ラベルを追加したLTR学習用データ。
        """
        
        for feature in features:
            feature.label = make_label(
                feature.doc_name,
                answers,
            )
            
def make_label(
    doc_name: str,
    answers: AnswerFiles,
) -> int:
    
    if doc_name in answers:
        return 1
    else:
        return 0
    
def keyword_match_count(
    document: str,
    query: QueryWords,
) -> int:
    """
    検索語と文書の一致数をカウントする。
    
    Parameters
    ----------
    document : str
        文書の単語リスト。
    query : list[str]
        検索語の単語リスト。
    
    Returns
    -------
    int
        検索語と文書の一致数。
    """
    
    return sum(
        document.count(word)
        for word in query
    )
    
    
def calculate_title_match(
    query_words: QueryWords,
    filename: str,
) -> float:
    
    title = filename.replace(
        ".pdf",
        ""
    )
    count = sum(
        word in title
        for word in query_words
    )
    
    return count / len(query_words)