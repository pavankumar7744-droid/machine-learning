from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
import os
from app.services.dataset_service import analyze_dataset
import json

router = APIRouter()

@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    if not file.filename.endswith(('.csv', '.xlsx')):
        raise HTTPException(status_code=400, detail="Only CSV and XLSX files are supported")
        
    contents = await file.read()
    file_id = str(uuid.uuid4())
    
    # Save file
    save_path = f"../data/uploads/{file_id}_{file.filename}"
    with open(save_path, "wb") as f:
        f.write(contents)
        
    try:
        analysis = analyze_dataset(contents, file.filename)
        analysis['id'] = file_id
        
        # Save analysis
        with open(f"../data/uploads/{file_id}_analysis.json", "w") as f:
            json.dump(analysis, f, indent=4)
            
        return analysis
    except Exception as e:
        # cleanup
        if os.path.exists(save_path):
            os.remove(save_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{dataset_id}/analysis")
def get_dataset_analysis(dataset_id: str):
    # Find the analysis file
    for file in os.listdir("../data/uploads"):
        if file.startswith(dataset_id) and file.endswith("_analysis.json"):
            with open(os.path.join("../data/uploads", file), "r") as f:
                return json.load(f)
    raise HTTPException(status_code=404, detail="Dataset not found")
