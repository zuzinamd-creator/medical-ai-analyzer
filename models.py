from pydantic import BaseModel
from typing import List, Dict, Union

class AnalysisResult(BaseModel):
    company_name: str
    product_category: str
    strengths: List[str]
    weaknesses: List[str]
    technical_specs: Dict[str, str]
    # Меняем int на str, чтобы ИИ мог писать пояснения
    design_score: Union[int, str] 
    market_potential: Union[int, str]
    overall_strategy: str