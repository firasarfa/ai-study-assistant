import requests
from bs4 import BeautifulSoup
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def load_url(url: str):
    """Scrapes plain text content from a webpage"""
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch {url}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # remove scripts/styles
    for script in soup(["script", "style", "noscript"]):
        script.decompose()
    
    text = soup.get_text(separator="\n")
    cleaned = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
    
    # wrap into LangChain-like Document
    return [{"page_content": cleaned, "metadata": {"source": url}}]



def load_chatgpt_share(url: str):
    """Scrape messages from a ChatGPT shared conversation"""
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch {url}")
    
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract all user + assistant messages
    messages = []
    for div in soup.find_all("div", attrs={"data-message-author-role": True}):
        role = div["data-message-author-role"]
        text = div.get_text(" ", strip=True)
        if text:
            messages.append(f"{role.upper()}: {text}")

    conversation = "\n".join(messages)
    return [{"page_content": conversation, "metadata": {"source": url}}]
