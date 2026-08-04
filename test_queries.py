test_queries = [

    # 完全一致
    (["独立行政法人"], ["sample.pdf"]),
    (["随意契約"], ["sample.pdf"]),
    (["企画競争"], ["sample.pdf"]),
    (["再就職"], ["sample.pdf"]),
    (["役員経験者"], ["sample.pdf"]),
    (["著作権"], ["ai_guideline.pdf"]),
    (["個人情報"], ["ai_guideline.pdf"]),
    (["禁止事項"], ["ai_guideline.pdf"]),
    (["教育情報課"], ["ai_guideline.pdf"]),
    (["成績評価"], ["ai_guideline.pdf"]),
    (["ディープラーニング"], ["G検定紹介資料_202606.pdf"]),
    (["エコシステム"], ["G検定紹介資料_202606.pdf"]),
    (["JDLA"], ["G検定紹介資料_202606.pdf"]),
    (["AI人材"], ["G検定紹介資料_202606.pdf"]),
    (["活用リテラシー"], ["G検定紹介資料_202606.pdf"]),
    (["AI倫理"], ["G検定紹介資料_202606.pdf"]),
    (["生成AI"], ["G検定紹介資料_202606.pdf"]),    
    (["機械学習"], ["machine_learning.pdf"]),
    (["データ分析"], ["machine_learning.pdf"]),
    (["正則化"], ["machine_learning.pdf"]),
    (["経験","学習"], ["machine_learning.pdf"]),
    (["訓練データ"], ["machine_learning.pdf"]),
    (["強化学習"], ["machine_learning.pdf"]),
    (["回帰"], ["machine_learning.pdf"]),
    (["分類"], ["machine_learning.pdf"]),
    (["損失関数"], ["machine_learning.pdf"]),

    # 人が検索しそう
    (["行政法人"], ["sample.pdf"]),
    (["再就職", "採用"],["sample.pdf"]),
    (["公表日"], ["sample.pdf"]),
    (["AI", "ルール"], ["ai_guideline.pdf"]),
    (["AI", "利用"], ["ai_guideline.pdf"]),
    (["学生", "AI"], ["ai_guideline.pdf"]),
    (["AI", "禁止"], ["ai_guideline.pdf"]),
    (["盗作"], ["ai_guideline.pdf"]),
    
    # 言い換え
    (["カテゴリ値"], ["machine_learning.pdf"]),
    (["離散値"], ["machine_learning.pdf"]),
    (["学生作品"], ["ai_guideline.pdf"]),
    (["レポート"], ["ai_guideline.pdf"]),
    (["Chat-GPT"], ["G検定紹介資料_202606.pdf"]),
    (["ChatGPT"], ["G検定紹介資料_202606.pdf"]),
    (["元職員"], ["sample.pdf"]),
    
    # 英語 ⇔ 日本語
    (["sepal.length", "がく弁の長さ"], ["machine_learning.pdf"]),
    (["生成AI", "ChatGPT"], ["ai_guideline.pdf", "G検定紹介資料_202606.pdf"]),
    
    
    # 曖昧検索
    (["契約方式"], ["sample.pdf"]),
    (["教材", "業務文書"], ["ai_guideline.pdf"]),
    
    # 複合語検索
    (["役員", "再就職"], ["sample.pdf"]),
    
    # 複数文書が正解
    (["ガイドライン"], ["G検定紹介資料_202606.pdf", "ai_guideline.pdf"]),
    (["ChatGPT"], ["ai_guideline.pdf", "G検定紹介資料_202606.pdf"]),
    (["情報"], ["sample.pdf", "ai_guideline.pdf", "G検定紹介資料_202606.pdf", "machine_learning.pdf"]),
   
]