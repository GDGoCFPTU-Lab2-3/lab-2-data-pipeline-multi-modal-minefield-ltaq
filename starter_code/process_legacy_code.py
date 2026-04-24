import ast

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract docstrings and comments from legacy Python code.

def extract_logic_from_code(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    # ------------------------------------------
    
    tree = ast.parse(source_code)
    extracted_logic = []
    
    # 1. Module level docstring
    module_doc = ast.get_docstring(tree)
    if module_doc:
        extracted_logic.append(f"Module Doc: {module_doc}")
        
    # 2. Function level docstrings
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            docstring = ast.get_docstring(node)
            if docstring:
                extracted_logic.append(f"Function '{node.name}' Logic: {docstring.strip()}")
                
    # 3. Find business rules in comments using regex
    rules = re.findall(r'#.*(Business Logic Rule \d+.*)', source_code, re.IGNORECASE)
    for rule in rules:
        extracted_logic.append(f"Comment Rule: {rule.strip()}")
        
    # Optional logic for detecting discrepancies (Role 3 might handle this too)
    if "tax_rate = 0.10" in source_code and "8%" in source_code:
        extracted_logic.append("ALERT: Potential tax rate discrepancy found between code and comments!")

    content_summary = "\n\n".join(extracted_logic)
    
    # 4. Return a dictionary for the UnifiedDocument schema
    return {
        "document_id": "code-legacy-001",
        "content": content_summary,
        "source_type": "Code",
        "author": "Senior Dev (retired)",
        "source_metadata": {
            "functions_found": [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)],
            "original_file": "legacy_pipeline.py"
        }
    }

# Nhớ import re vì ta sử dụng nó ở đây
import re

