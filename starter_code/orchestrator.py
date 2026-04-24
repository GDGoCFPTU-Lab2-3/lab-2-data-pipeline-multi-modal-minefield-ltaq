import json
import time
import os

# Robust path handling
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "raw_data")


# Import role-specific modules
from schema import UnifiedDocument
from process_pdf import extract_pdf_data
from process_transcript import clean_transcript
from process_html import parse_html_catalog
from process_csv import process_sales_csv
from process_legacy_code import extract_logic_from_code
from quality_check import run_quality_gate

# ==========================================
# ROLE 4: DEVOPS & INTEGRATION SPECIALIST
# ==========================================
# Task: Orchestrate the ingestion pipeline and handle errors/SLA.

def main():
    start_time = time.time()
    final_kb = []
    
    # --- FILE PATH SETUP (Handled for students) ---
    pdf_path = os.path.join(RAW_DATA_DIR, "lecture_notes.pdf")
    trans_path = os.path.join(RAW_DATA_DIR, "demo_transcript.txt")
    html_path = os.path.join(RAW_DATA_DIR, "product_catalog.html")
    csv_path = os.path.join(RAW_DATA_DIR, "sales_records.csv")
    code_path = os.path.join(RAW_DATA_DIR, "legacy_pipeline.py")
    
    output_path = os.path.join(os.path.dirname(SCRIPT_DIR), "processed_knowledge_base.json")
    
    # --- PROCESSING PIPELINE ---
    print("Starting Multi-Modal Pipeline...")
    
    # 1. Process PDF (May fail if API key is missing)
    try:
        pdf_data = extract_pdf_data(pdf_path)
        if pdf_data:
            # We wrap it in UnifiedDocument for validation
            doc = UnifiedDocument(**pdf_data)
            if run_quality_gate(doc.model_dump()):
                final_kb.append(doc.model_dump())
    except Exception as e:
        print(f"Error processing PDF: {e}")

    # 2. Process CSV
    csv_docs = process_sales_csv(csv_path)
    for doc_dict in csv_docs:
        if run_quality_gate(doc_dict):
            final_kb.append(doc_dict)

    # 3. Process HTML
    html_docs = parse_html_catalog(html_path)
    for doc_dict in html_docs:
        if run_quality_gate(doc_dict):
            final_kb.append(doc_dict)

    # 4. Process Transcript
    trans_data = clean_transcript(trans_path)
    if trans_data and run_quality_gate(trans_data):
        final_kb.append(trans_data)

    # 5. Process Legacy Code
    code_data = extract_logic_from_code(code_path)
    if code_data and run_quality_gate(code_data):
        final_kb.append(code_data)

    # --- SAVE RESULTS ---
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_kb, f, ensure_ascii=False, indent=4, default=str)

    end_time = time.time()
    duration = end_time - start_time
    print("-" * 30)
    print(f"Pipeline finished in {duration:.2f} seconds.")
    print(f"Total valid documents stored in KB: {len(final_kb)}")
    
    if duration > 30:
        print("SLA WARNING: Processing took longer than 30 seconds!")
    else:
        print("SLA PASSED: Real-time ingestion successful.")


if __name__ == "__main__":
    main()
