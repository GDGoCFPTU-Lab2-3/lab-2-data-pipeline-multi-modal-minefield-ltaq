# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================
# Task: Implement quality gates to reject corrupt data or logic discrepancies.

def run_quality_gate(document_dict):
    """
    Kiểm tra chất lượng tài liệu trước khi đưa vào Knowledge Base.
    """
    content = document_dict.get("content", "")
    
    # 1. Reject documents with 'content' length < 20 characters
    if len(content) < 20:
        print(f"Rejected: Document {document_dict.get('document_id')} content too short.")
        return False
        
    # 2. Reject documents containing toxic/error strings
    toxic_keywords = ['Null pointer exception', 'Access denied', 'FATAL ERROR', 'Traceback']
    for kw in toxic_keywords:
        if kw.lower() in content.lower():
            print(f"Rejected: Document {document_dict.get('document_id')} contains error/toxic string: '{kw}'.")
            return False
            
    # 3. Flag discrepancies (Simple logic example)
    # Ví dụ: Nếu trong code có nhắc đến thuế nhưng sai số liệu (có thể mở rộng thêm)
    
    return True
