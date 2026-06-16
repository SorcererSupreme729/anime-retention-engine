from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

model = joblib.load('anime_model.pkl')
model_columns = joblib.load('model_columns.pkl')

class AnimeIdea(BaseModel):
    episodes: int
    score: float
    source: str
    season: str
    studio: str
    genres: list[str]

@app.post("/simulate")
def run_simulation(anime: AnimeIdea):
    input_data = pd.DataFrame(0, index=[0], columns=model_columns)
    
    input_data['episodes'] = anime.episodes
    input_data['score'] = anime.score
    
    if f"source_{anime.source}" in model_columns:
        input_data[f"source_{anime.source}"] = 1
    if f"season_{anime.season}" in model_columns:
        input_data[f"season_{anime.season}"] = 1
    if f"studios_{anime.studio}" in model_columns:
        input_data[f"studios_{anime.studio}"] = 1
        
    for genre in anime.genres:
        if genre in model_columns:
            input_data[genre] = 1
            
    hit_prob = float(model.predict_proba(input_data)[0][1])
    weekly_ret_rate = float(0.70 + (0.25 * hit_prob))
    
    viewers = [10000]
    for _ in range(2, 13):
        viewers.append(int(viewers[-1] * weekly_ret_rate))
        
    return {
        "message": "Simulation Complete",
        "hit_probability": hit_prob,
        "weekly_retention": weekly_ret_rate,
        "curve": viewers
    }