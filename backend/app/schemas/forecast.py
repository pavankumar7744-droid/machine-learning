from pydantic import BaseModel
from typing import Optional, List

class ForecastConfigureRequest(BaseModel):
    dataset_id: str
    date_column: str
    sales_metric: str
    group_column: Optional[str] = None
    specific_group: Optional[str] = None
    frequency: str = 'D'
    forecast_horizon: int
    model: str # 'XGBoost' or 'LightGBM'

class ForecastRecord(BaseModel):
    date: str
    group: Optional[str]
    forecast: float

class ForecastResponse(BaseModel):
    forecast_id: str
    summary: dict
    forecasts: List[ForecastRecord]
