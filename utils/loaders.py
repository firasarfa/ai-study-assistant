import requests
from bs4 import BeautifulSoup
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from load_url import load_chatgpt_share , load_url

def load_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    return loader.load()

def load_docx(file_path: str):
    loader = Docx2txtLoader(file_path)
    return loader.load()

def load_txt(file_path: str):
    loader = TextLoader(file_path, encoding="utf-8")
    return loader.load()

def load_file(file_path: str):
    if file_path.endswith(".pdf"):
        return load_pdf(file_path)
    elif file_path.endswith(".docx"):
        return load_docx(file_path)
    elif file_path.endswith(".txt"):
        return load_txt(file_path)
    else:
        raise ValueError("Unsupported file format")


def smart_loader(link_or_file):
    if link_or_file.startswith("http") and "chatgpt.com/share" in link_or_file:
        return load_chatgpt_share(link_or_file)
    elif link_or_file.startswith("http"):
        return load_url(link_or_file)
    else:
        return load_file(link_or_file)