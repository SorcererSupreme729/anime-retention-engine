# 🎬 Anime Viewer Retention Predictor

🚀 **Live Simulation:** [Render](https://anime-retention-engine.onrender.com/)

📊 **Dataset:** [Historical Anime Production & Audience Metrics](https://www.kaggle.com/datasets/sazzadsiddiquelikhon/myanimelist-anime-database-july-2025)

---

## The Idea

I built a "what-if" simulation to explore how pre-production factors influence weekly audience retention. 
Input the studio, genre, source material, and your rating estimate. 
My XGBoost model generates a real-time drop-off curve.

It's also interesting to run it against already aired anime to see how closely the projections match actual trends. 
Sometimes it nails it, sometimes it doesn't which is honestly half the fun.

Anime v1 is live, and the pipeline is ready for web series next.

---

## Features

* 📊 Simulates weekly viewer drop-off across a full season
* 🧠 Real-time predictions based on studio, genre, source, and rating inputs
* 🎛️ Interactive dashboard to tweak parameters and see curves update instantly
* 📈 Clean, dark-mode UI
* ⚡ Deployed with a lightweight architecture to avoid cold-start delays
* 🎨 Also works on already aired anime, so you can test if the model's actually onto something

---

## Model Architecture & Logic

### 1. The Inference Engine

This uses XGBoost because it handles categories well and doesn't assume a straight-line relationship between inputs and output.
The model takes these inputs:

* **Production Vectors:** Studio, Source Material
* **Temporal Indicators:** Release Season
* **Quality Baseline:** Historical Score Metrics
* **Content Matrix:** Multi-label Genre tags

### 2. The Mechanics

The model outputs a hit probability. That number then goes into a custom decay formula to figure out weekly retention:

'weekly_retention_rate = 0.70 + (0.25 * hit_probability)'

This gives a retention percentage for each episode. 
I then apply it cumulatively across the season—so episode 1 starts at 100%, episode 2 drops based on this rate, episode 3 drops further, and so on. 
The final curve is what shows up on the frontend.

### 3. Production Architecture

I started with a separate FastAPI backend and a Dash frontend. 
But on free hosting, the container kept timing out. 
So instead of using the API in production, I embedded the model directly into the frontend callbacks. 
The API code is still in the repo, just not used in the live version.

Here's how it works now :
The model file (anime_model.pkl) loads into memory using joblib when the server starts.
Instead of making external API calls, the Dash callbacks directly run the model locally.
User inputs get validated, converted, and passed to the model.

---

## Technologies Used

* Python
* Pandas
* NumPy
* XGBoost
* Scikit-Learn
* Joblib
* Plotly Dash
* Dash Bootstrap Components

---

## Future Plans

* Real-time API data scraping (Jikan / AniList / MAL)
* Multi-season retention modeling
* Web series mode, so the tool isn't just for anime nerds
* Interactive session tracking to compare multiple retention curves simultaneously
