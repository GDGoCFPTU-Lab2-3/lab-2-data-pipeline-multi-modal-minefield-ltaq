from bs4 import BeautifulSoup

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract product data from the HTML table, ignoring boilerplate.

def parse_html_catalog(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    # ------------------------------------------
    
    # 1. Find the table with id 'main-catalog'
    table = soup.find('table', id='main-catalog')
    if not table:
        return []
        
    documents = []
    rows = table.find('tbody').find_all('tr')
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 4:
            continue
            
        sp_id = cols[0].text.strip()
        name = cols[1].text.strip()
        category = cols[2].text.strip()
        price_raw = cols[3].text.strip()
        stock = cols[4].text.strip()
        rating = cols[5].text.strip() if len(cols) > 5 else "N/A"
        
        # 2. Extract rows, handling 'N/A' or 'Liên hệ' in the price column
        is_available = price_raw not in ['N/A', 'Liên hệ']
        
        # 3. Return a list of dictionaries for the UnifiedDocument schema
        doc = {
            "document_id": f"html-prod-{sp_id}",
            "content": f"Product: {name}, Category: {category}, Price: {price_raw}, Stock: {stock}, Rating: {rating}",
            "source_type": "HTML",
            "author": "VinShop Catalog",
            "source_metadata": {
                "sku": sp_id,
                "is_available": is_available,
                "original_file": "product_catalog.html"
            }
        }
        documents.append(doc)
    
    return documents

