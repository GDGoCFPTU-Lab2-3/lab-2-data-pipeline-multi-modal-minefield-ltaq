from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ==========================================
# ROLE 1: LEAD DATA ARCHITECT
# ==========================================
# Your task is to define the Unified Schema for all sources.
# This is v1. Note: A breaking change is coming at 11:00 AM!

class UnifiedDocument(BaseModel):
    """
    Schema thống nhất cho v1 của Knowledge Base.
    """
    document_id: str = Field(..., description="ID duy nhất cho tài liệu, ví dụ: pdf-001")
    content: str = Field(..., description="Nội dung văn bản đã được trích xuất hoặc làm sạch")
    source_type: str = Field(..., description="Loại nguồn: PDF, Transcript, HTML, CSV, hoặc Code")
    author: Optional[str] = Field("Unknown", description="Tác giả của tài liệu nếu có")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="Thời điểm xử lý hoặc thời gian gốc của tài liệu")
    
    # Metadata linh hoạt cho từng loại nguồn cụ thể
    source_metadata: dict = Field(
        default_factory=dict, 
        description="Thông tin bổ sung như tên tệp gốc, số dòng, URL, v.v."
    )
