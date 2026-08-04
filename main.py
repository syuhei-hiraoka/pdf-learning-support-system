from summarizer import extract_keywords
from pdf_loader import load_pdf_files
from search_types import test_queries
from evaluation import evaluate_all
from normalize_text import normalize_text
from query_expansion import (
    expand_query,
    get_query_words,
)    
from resources import create_search_resources
from result import (
    make_search_results, 
    display_preprocess_results,
    display_query,
    display_title,
    display_results,
)
from search import search_all


PDF_FOLDER = "pdfs"

        
def main():
    """
    ターミナル版検索システム。
    
    PDFをアップロードし、検索語を入力すると、
    関連する情報が抽出される。
    
    """
    texts, pdf_files = load_pdf_files(PDF_FOLDER)

    resources = create_search_resources(
        texts,
        pdf_files,
        test_queries,
    )
    display_preprocess_results(resources)        
    evaluate_all(resources, test_queries)

    while True:
        text = input("検索語を入力(exitで終了): ")
        
        text = normalize_text(text)
        
        if text == "exit":
            break
        
        # 検索用
        query = extract_keywords(text, filename=None)
        query = expand_query(query)
        
        query_words = get_query_words(query)
        
        if not query:
            print("検索語を入力してください")
            continue

        display_query(query_words)
        results = search_all(query_words, resources)
        for title, result in results.items():
            
            display_title(title)
            search_results = make_search_results(
                result,
                query_words,
                resources,
            )
            for result in search_results:
                display_results(result)
            
if __name__ == "__main__":
    main()