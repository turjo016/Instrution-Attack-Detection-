from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

# ==========================================
# SAFE MODEL PATH
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "attack_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")

# ==========================================
# LOAD MODEL
# ==========================================
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

print("✅ Model Loaded Successfully")

# ==========================================
# FASTAPI APP
# ==========================================
app = FastAPI(
    title="AI IDS API",
    version="1.0"
)

# ==========================================
# INPUT FORMAT
# ==========================================
class TrafficData(BaseModel):
    features: list

# ==========================================
# HOME ROUTE
# ==========================================
@app.get("/")
def home():

    return {
        "message": "🚀 FastAPI IDS Running"
    }

# ==========================================
# PREDICTION ROUTE
# ==========================================
@app.post("/predict")
def predict(data: TrafficData):

    try:

        # Convert input
        features = np.array(
            data.features
        ).reshape(1, -1)

        # Scale
        scaled_data = scaler.transform(features)

        # Predict
        prediction = model.predict(scaled_data)[0]

        # Probability
        probability = float(
            model.predict_proba(scaled_data)[0][1]
        )

        # Risk level
        if probability < 0.3:
            risk = "LOW"

        elif probability < 0.7:
            risk = "MEDIUM"

        else:
            risk = "HIGH"

        # Final result
        result = {

            "prediction": int(prediction),

            "confidence_score":
                round(probability, 4),

            "risk_level": risk,

            "status":
                "🚨 ATTACK DETECTED"
                if prediction == 1
                else "✅ NORMAL TRAFFIC"
        }

        return result

    except Exception as e:

        return {
            "error": str(e)
        }