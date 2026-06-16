import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import requests
import plotly.graph_objs as go

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

sidebar = html.Div([
    html.H4("⚙️ Settings", className="text-info"),
    html.Hr(),
    html.Label("Episodes:"),
    dbc.Input(id='input-episodes', type='number', value=12, className="mb-3"),

    html.Label("Source MAL Score (1-10):"),
    dbc.Input(id='input-score', type='number', value=8.0, step=0.1, className="mb-3"),
    
    html.Label("Source:"),
    dcc.Dropdown(id='input-source', options=['Manga', 'Original', 'Light novel', 'Visual novel'], value='Manga', className="mb-3 text-dark"),
    
    html.Label("Season:"),
    dcc.Dropdown(id='input-season', options=['spring', 'summer', 'fall', 'winter'], value='spring', className="mb-3 text-dark"),
    
    html.Label("Studio:"),
    dcc.Dropdown(id='input-studio', options=['MAPPA', 'Ufotable', 'Madhouse', 'Kyoto Animation', 'Bones', 'Toei Animation', 'Studio Ghibli', 'Wit Studio', 'A-1 Pictures', 'Studio Pierrot', 'Studio Trigger'], value='MAPPA', className="mb-3 text-dark"),
    
    html.Label("Genres (comma separated):"),
    dbc.Input(id='input-genres', type='text', value='Action, Fantasy', className="mb-4"),
    
    dbc.Button('🚀 Run Simulation', id='submit-button', color="info", className="w-100")
], style={"padding": "20px", "background-color": "#111111", "border-radius": "10px"})

app.layout = dbc.Container([
    dbc.Row([
        html.H1("🎬 Anime Retention Predictor", className="text-center my-4 text-white")
    ]),
    
    dbc.Row([
        dbc.Col(sidebar, width=3),
        
        dbc.Col([
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H5("AI Hit Probability", className="text-muted"),
                        html.H2(id="out-prob", className="text-success text-center")
                    ])
                ], color="dark", outline=True), width=6),
                
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H5("Expected Finale Viewers", className="text-muted"),
                        html.H2(id="out-viewers", className="text-info text-center")
                    ])
                ], color="dark", outline=True), width=6),
            ], className="mb-4"),
            
            dbc.Card(dcc.Graph(id='output-graph'), body=True, color="dark")
            
        ], width=9)
    ])
], fluid=True, style={"background-color": "#000000", "min-height": "100vh", "padding": "20px"})

@app.callback(
    [Output('output-graph', 'figure'),
     Output('out-prob', 'children'),
     Output('out-viewers', 'children')],
    [Input('submit-button', 'n_clicks')],
    [State('input-episodes', 'value'),
     State('input-score', 'value'),
     State('input-source', 'value'),
     State('input-season', 'value'),
     State('input-studio', 'value'),
     State('input-genres', 'value')]
)
def update_graph(n_clicks, episodes, score, source, season, studio, genres_text):
    if n_clicks == 0:
        return dash.no_update, "", ""
        
    genre_list = [g.strip() for g in genres_text.split(',')]
    
    payload = {
        "episodes": episodes,
        "source": source,
        "score": score,
        "season": season,
        "studio": studio,
        "genres": genre_list
    }
    
    response = requests.post('http://127.0.0.1:8000/simulate', json=payload)
    data = response.json()
    
    curve = data['curve']
    hit_prob = data['hit_probability']
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(1, 13)), y=curve, mode='lines+markers', name='Viewers', line=dict(color='#00f2fe', width=3)))
    fig.update_layout(
        title="Projected Viewer Retention", 
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Episode", 
        yaxis_title="Active Viewers", 
        yaxis_range=[0, 10500]
    )
    
    prob_text = f"{int(hit_prob * 100)}%"
    viewer_text = f"{curve[-1]:,}"
    
    return fig, prob_text, viewer_text

if __name__ == '__main__':
    app.run(debug=True, port=8050)