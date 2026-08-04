from __future__ import annotations
from search_types import Query
from search import (
    make_rrf_inputs,
    make_ltr_inputs,
)
from feature_builder import FeatureBuilder
from learning_to_rank import LearningToRank

def train_ltr(
    queries: list[Query],
    resources: "SearchResources",
) -> LearningToRank:
    X_all = []
    y_all = []
    builder = FeatureBuilder()
    ltr = LearningToRank()
    for query in queries:
        ltr_inputs = make_rrf_inputs(
            query.words,
            resources.bm25,
            resources.joined_docs,
            resources.vector,
        )
        rrf_results = resources.rrf.search(ltr_inputs)
        ltr_inputs = make_ltr_inputs(ltr_inputs, rrf_results)
        features = builder.build(
            query.words,
            ltr_inputs,
            resources.body_texts,
            resources.pdf_files,
        )
        builder.add_labels(features, query.answers)
        X, y = builder.to_dataset(features)
        X_all.extend(X)
        y_all.extend(y)
    
    ltr.fit(X_all, y_all)
    
    return ltr