from fastapi import APIRouter, HTTPException
import os
import json
from app.schemas.forecast import ForecastConfigureRequest, ForecastResponse
from app.services.forecasting_service import run_forecast

router = APIRouter()

@router.post("/run", response_model=ForecastResponse)
def generate_forecast(request: ForecastConfigureRequest):
    # Find dataset file
    file_path = None
    for file in os.listdir("../data/uploads"):
        if file.startswith(request.dataset_id) and not file.endswith("_analysis.json"):
            file_path = os.path.join("../data/uploads", file)
            break
            
    if not file_path:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    try:
        result = run_forecast(request, file_path)
        
        # Save forecast to results
        os.makedirs("../results/forecasts", exist_ok=True)
        with open(f"../results/forecasts/{result['forecast_id']}.json", "w") as f:
            json.dump(result, f, indent=4)
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
