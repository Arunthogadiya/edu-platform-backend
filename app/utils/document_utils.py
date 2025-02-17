from langchain_community.document_loaders import TextLoader, PDFLoader, DocxLoader
from typing import List
from langchain.schema import Document
import os

def load_documents(file_path: str) -> List[Document]:
    """Load documents based on file type"""
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.txt':
        loader = TextLoader(file_path)
    elif file_extension == '.pdf':
        loader = PDFLoader(file_path)
    elif file_extension in ['.doc', '.docx']:
        loader = DocxLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")
        
    return loader.load()

def format_docs(docs: List[Document]) -> str:
    """Convert documents to string format"""
    return "\n\n".join(doc.page_content for doc in docs)
