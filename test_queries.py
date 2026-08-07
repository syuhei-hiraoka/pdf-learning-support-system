test_queries = [

    # 完全一致
    (["独立行政法人"], ["sample.pdf"]),
    (["随意契約"], ["sample.pdf"]),
    (["企画競争"], ["sample.pdf"]),
    (["再就職"], ["sample.pdf"]),
    (["役員経験者"], ["sample.pdf"]),
    (["著作権"], ["sample_ai_guideline.pdf"]),
    (["個人情報"], ["sample_ai_guideline.pdf"]),
    (["禁止事項"], ["sample_ai_guideline.pdf"]),
    (["教育情報課"], ["sample_ai_guideline.pdf"]),
    (["成績評価"], ["sample_ai_guideline.pdf"]),
    (["ディープラーニング"], ["sample_exam.pdf"]),
    (["エコシステム"], ["sample_exam.pdf"]),
    (["JDLA"], ["sample_exam.pdf"]),
    (["AI人材"], ["sample_exam.pdf"]),
    (["活用リテラシー"], ["sample_exam.pdf"]),
    (["AI倫理"], ["sample_exam.pdf"]),
    (["生成AI"], ["sample_exam.pdf"]),    
    (["機械学習"], ["sample_ml.pdf"]),
    (["データ分析"], ["sample_ml.pdf"]),
    (["正則化"], ["sample_ml.pdf"]),
    (["経験","学習"], ["sample_ml.pdf"]),
    (["訓練データ"], ["sample_ml.pdf"]),
    (["強化学習"], ["sample_ml.pdf"]),
    (["回帰"], ["sample_ml.pdf"]),
    (["分類"], ["sample_ml.pdf"]),
    (["損失関数"], ["sample_ml.pdf"]),

    # 人が検索しそう
    (["行政法人"], ["sample.pdf"]),
    (["再就職", "採用"],["sample.pdf"]),
    (["公表日"], ["sample.pdf"]),
    (["AI", "ルール"], ["sample_ai_guideline.pdf"]),
    (["AI", "利用"], ["sample_ai_guideline.pdf"]),
    (["学生", "AI"], ["sample_ai_guideline.pdf"]),
    (["AI", "禁止"], ["sample_ai_guideline.pdf"]),
    (["盗作"], ["sample_ai_guideline.pdf"]),
    
    # 言い換え
    (["カテゴリ値"], ["sample_ml.pdf"]),
    (["離散値"], ["sample_ml.pdf"]),
    (["学生作品"], ["sample_ai_guideline.pdf"]),
    (["レポート"], ["sample_ai_guideline.pdf"]),
    (["Chat-GPT"], ["sample_exam.pdf"]),
    (["ChatGPT"], ["sample_exam.pdf"]),
    (["元職員"], ["sample.pdf"]),
    
    # 英語 ⇔ 日本語
    (["sepal.length", "がく弁の長さ"], ["sample_ml.pdf"]),
    (["生成AI", "ChatGPT"], ["sample_ai_guideline.pdf", "sample_exam.pdf"]),
    
    
    # 曖昧検索
    (["契約方式"], ["sample.pdf"]),
    (["教材", "業務文書"], ["sample_ai_guideline.pdf"]),
    
    # 複合語検索
    (["役員", "再就職"], ["sample.pdf"]),
    
    # 複数文書が正解
    (["ガイドライン"], ["sample_exam.pdf", "sample_ai_guideline.pdf"]),
    (["ChatGPT"], ["sample_ai_guideline.pdf", "sample_exam.pdf"]),
    (["情報"], ["sample.pdf", "sample_ai_guideline.pdf", "sample_exam.pdf", "sample_ml.pdf"]),
   
]