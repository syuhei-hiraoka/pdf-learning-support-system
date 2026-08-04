from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from feature_builder import FeatureBuilder
from search_types import (
    ListScores,
    JudgeScores,
    SearchScores,
    Feature,
)

        
class LearningToRank:
    
    def __init__(
        self,
    ):
        self.scaler = StandardScaler()
        self.model = LogisticRegression()
        self.feature_builder = FeatureBuilder()
        
    
    def fit(
        self, 
        X: list[ListScores], 
        y: JudgeScores,
    ):
        X_scaled = self.scaler.fit_transform(X)
        
        self.model.fit(X_scaled, y)
    
    def predict(
        self,
       features: list[Feature],
    ) ->SearchScores:
        
        X = self.feature_builder.make_X(features)
        X_scaled = self.scaler.transform(X)
        scores = self.model.predict_proba(X_scaled)[:, 1]
        results = [
            (feature.doc_id, score)
            for feature, score in zip(features, scores)
        ]
            
        predict_results = sorted(
            results,
            key=lambda result: result[1],
            reverse=True
        )
        return predict_results
    