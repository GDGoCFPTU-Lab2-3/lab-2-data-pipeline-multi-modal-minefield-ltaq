import pandas as pd

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Process sales records, handling type traps and duplicates.

def process_sales_csv(file_path):
    # --- FILE READING (Handled for students) ---
    df = pd.read_csv(file_path)
    # ------------------------------------------
    
    # 1. Remove duplicate rows based on 'id'
    df = df.drop_duplicates(subset=['id'], keep='first')
    
    # 2. Clean 'price' column
    def clean_price(val):
        if pd.isna(val) or str(val).upper() == 'N/A':
            return 0.0
        # Remove symbols like $ or ,
        clean_val = str(val).replace('$', '').replace(',', '')
        try:
            return float(clean_val)
        except ValueError:
            # Handle cases like "five dollars" if necessary, or just return 0.0
            return 0.0
            
    df['price'] = df['price'].apply(clean_price)
    
    # 3. Normalize 'date_of_sale'
    def normalize_date(val):
        try:
            # pandas to_datetime handles most common formats automatically
            return pd.to_datetime(val, dayfirst=True).strftime('%Y-%m-%d')
        except:
            return None
            
    df['date_of_sale'] = df['date_of_sale'].apply(normalize_date)
    
    # 4. Return a list of dictionaries for the UnifiedDocument schema
    documents = []
    for _, row in df.iterrows():
        doc = {
            "document_id": f"csv-sale-{row['id']}",
            "content": f"Product: {row['product_name']}, Category: {row['category']}, Price: {row['price']} {row['currency']}",
            "source_type": "CSV",
            "author": f"Seller {row['seller_id']}",
            "timestamp": row['date_of_sale'],
            "source_metadata": {
                "stock_quantity": row['stock_quantity'],
                "original_file": "sales_records.csv"
            }
        }
        documents.append(doc)
    
    return documents

