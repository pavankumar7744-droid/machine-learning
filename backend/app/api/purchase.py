import uuid
from fastapi import APIRouter, HTTPException
import joblib
import pandas as pd
from app.schemas.purchase import PurchasePredictionRequest, PurchasePredictionResponse
import os
from app.ml.feature_engineering import engineer_purchase_features # we need to write this

router = APIRouter()

# Load models at startup
models = {}

def load_models():
    base_dir = "../models/purchase/"
    for model in ['xgboost', 'lightgbm']:
        for variant in ['full', 'no_pagevalues']:
            path = os.path.join(base_dir, f"{model}_{variant}.joblib")
            if os.path.exists(path):
                models[f"{model}_{variant}"] = joblib.load(path)

load_models()

@router.post("/predict", response_model=PurchasePredictionResponse)
def predict_purchase(request: PurchasePredictionRequest):
    model_key = f"{request.model_type.lower()}_{request.variant.lower()}"
    
    if model_key not in models:
        raise HTTPException(status_code=400, detail="Requested model/variant not available")
        
    model = models[model_key]
    
    # Construct DF
    input_dict = request.model_dump(exclude={'model_type', 'variant'})
    df = pd.DataFrame([input_dict])
    
    # Engineer features
    df_eng = engineer_purchase_features(df)
    
    # Predict
    prob = model.predict_proba(df_eng)[0][1]
    
    # The thresholds should ideally be loaded. For now, simple 0.5.
    threshold = 0.5
    prediction = "Purchase" if prob >= threshold else "No Purchase"
    
    return PurchasePredictionResponse(
        prediction_id=str(uuid.uuid4()),
        prediction=prediction,
        purchase_probability=prob,
        non_purchase_probability=1 - prob,
        model=request.model_type,
        variant=request.variant,
        threshold=threshold
    )
