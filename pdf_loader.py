from pypdf import PdfReader
import os
from search_types import(
    PdfData,
    PdfPages,
    PdfData,
    PdfFiles,
)

def extract_pdf_text(pdf) -> PdfPages:
    """
    PDFから全文を抽出する
    
    Parameters
    ----------
    pdf : str | BinaryIO
        PDFファイルのパスまたはUploadedFile
        
    Returns
    -------
    PdfPages
        抽出した全文
    """
    
    reader: PdfReader = PdfReader(pdf)
    texts: PdfPages = []
    
    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()
        if page_text:
            page_data = {
                "page": page_number,
                "text": page_text,
            }
            texts.append(page_data)
            
    return texts
        
def load_pdf_files(folder_path: str ="pdfs") -> PdfData:
    """
    指定したフォルダ内のPDFを読み込む
    
    Parameters
    ----------
    folder_path : str
        PDFファイルが保存されているフォルダのパス
    
    Returns
    -------
    PdfData
        抽出したテキストのリストとPDFファイル名のリスト
    """
    texts: list[PdfPages] = []
    pdf_files: list[str] = []
    
    for filename in sorted(os.listdir(folder_path)):
        
        if not filename.endswith(".pdf"):
            continue
        
        path = os.path.join(folder_path, filename)
        print("読み込み中:", path)
        
        try:
            pages = extract_pdf_text(path)
                    
            texts.append(pages)
            pdf_files.append(filename)
            
        except Exception as e:
            print(f"{filename} 読み込み失敗: {e}")

    return texts, pdf_files

def load_uploaded_pdfs(uploaded_files) -> PdfData:
    """
    StreamlitでアップロードされたPDFを読み込む
    
    Parameters
    ----------
    uploaded_files
        StreamlitのUploadedFileのリスト
        
    Returns
    -------
    PdfData
        抽出したテキストのリストとPDFファイル名のリスト
    """
    texts: list[PdfPages] = []
    pdf_files: PdfFiles = []
    
    if not uploaded_files:
        return [], []
    
    for uploaded_file in uploaded_files:
        if not uploaded_file.name.endswith(".pdf"):
            continue
        
        try:
            pages = extract_pdf_text(uploaded_file)
            
            texts.append(pages)
            pdf_files.append(uploaded_file.name)
        
        except Exception as e:
            print(f"{uploaded_file.name} の読み込みに失敗: {e}")
            
    return texts, pdf_files

def pages_to_text(pages: PdfPages) -> str:
    """PDFファイルから文字列を取得する。
    
    Parameters
    ----------
    pages : PdfPages
        PDFのページ内の情報。
    
    Returns
    -------
        PDFからページごとのテキスト情報を取得。
    """
    page_texts = [
        page["text"]
        for page in pages
    ]
    return " ".join(page_texts)