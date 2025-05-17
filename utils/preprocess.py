import re
from typing import List

def clean_text(text: str) -> str:
    """Clean and normalize text for processing"""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.,;!?]', '', text)
    return text.strip()

def chunk_text(text: str, chunk_size: int = 1000) -> List[str]:
    """Split text into chunks of approximately chunk_size characters"""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 > chunk_size and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_length = 0
        
        current_chunk.append(word)
        current_length += len(word) + 1
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks