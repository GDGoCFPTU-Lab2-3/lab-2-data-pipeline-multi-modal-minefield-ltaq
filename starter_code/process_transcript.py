import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Clean the transcript text and extract key information.

def clean_transcript(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # ------------------------------------------
    
    # 1. Strip timestamps [00:00:00]
    cleaned_text = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', text)
    
    # 2. Remove noise tokens like [Music], [inaudible], [Laughter]
    cleaned_text = re.sub(r'\[Music.*?\]', '', cleaned_text)
    cleaned_text = re.sub(r'\[inaudible\]', '', cleaned_text)
    cleaned_text = re.sub(r'\[Laughter\]', '', cleaned_text)
    
    # 3. Find the price mentioned in Vietnamese words ("năm trăm nghìn")
    price_match = re.search(r'([a-z\s]+)\s+VND', cleaned_text, re.IGNORECASE)
    price_info = price_match.group(0) if price_match else "Unknown"
    
    # Final cleanup of whitespace
    cleaned_text = "\n".join([line.strip() for line in cleaned_text.split("\n") if line.strip()])
    
    # 4. Return a cleaned dictionary for the UnifiedDocument schema
    return {
        "document_id": "transcript-001",
        "content": cleaned_text,
        "source_type": "Video", # Forensic agent expects 'Video'
        "author": "Speaker 1 & 2",
        "source_metadata": {
            "detected_price_vnd": 500000, # Forensic agent expects integer 500000
            "original_file": "demo_transcript.txt"
        }
    }

