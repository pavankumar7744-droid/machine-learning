from pydantic import BaseModel
from typing import Optional

class PurchasePredictionRequest(BaseModel):
    Administrative: int
    Administrative_Duration: float
    Informational: int
    Informational_Duration: float
    ProductRelated: int
    ProductRelated_Duration: float
    BounceRates: float
    ExitRates: float
    PageValues: float
    SpecialDay: float
    Month: str
    OperatingSystems: int
    Browser: int
    Region: int
    TrafficType: int
    VisitorType: str
    Weekend: bool
    
    model_type: str # 'XGBoost' or 'LightGBM'
    variant: str # 'Full' or 'No_PageValues'

class PurchasePredictionResponse(BaseModel):
    prediction_id: str
    prediction: str
    purchase_probability: float
    non_purchase_probability: float
    model: str
    variant: str
    threshold: float
