import pandas as pd
from dash import Dash, html, dcc, dash_table, Input, Output
import plotly.express as px
import os

# Load data
DATA_PATH = "data/output_bersih/combined_cleaned_data.csv"
df = pd.read_csv(DATA_PATH)

# Preprocessing kolom waktu jika ada
if 'STA (WIB)' in df.columns:
    df['STA (WIB)'] = pd.to_datetime(df['STA (WIB)'], errors='coerce').dt.time
if 'STD (WIB)' in df.columns:
    df['STD (WIB)'] = pd.to_datetime(df['STD (WIB)'], errors='coerce').dt.time

# App init
app = Dash(__name__)
app.title = "Dashboard Penerbangan"

# Layout
app.layout = html.Div([
    html.H1("📊 Dashboard Penerbangan", style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.Label("Pilih Maskapai:"),
            dcc.Dropdown(
                options=[{"label": m, "value": m} for m in sorted(df['AIRLINE'].unique())],
                id="maskapai-dropdown",
                multi=True
            ),
        ], style={"width": "30%", "display": "inline-block", "padding": "10px"}),

        html.Div([
            html.Label("Pilih Bandara Asal:"),
            dcc.Dropdown(
                options=[{"label": a, "value": a} for a in sorted(df['ORIGIN AIRPORT'].unique())],
                id="bandara-dropdown",
                multi=True
            ),
        ], style={"width": "30%", "display": "inline-block", "padding": "10px"}),
    ]),

    dcc.Graph(id="grafik-jumlah-penerbangan"),

    html.H3("📋 Tabel Data Penerbangan"),
    dash_table.DataTable(
        id="tabel-penerbangan",
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=10,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left", "minWidth": "100px"}
    )
])

# Callback
@app.callback(
    [Output("grafik-jumlah-penerbangan", "figure"),
     Output("tabel-penerbangan", "data")],
    [Input("maskapai-dropdown", "value"),
     Input("bandara-dropdown", "value")]
)
def update_dashboard(selected_maskapai, selected_bandara):
    filtered_df = df.copy()

    if selected_maskapai:
        filtered_df = filtered_df[filtered_df['AIRLINE'].isin(selected_maskapai)]
    if selected_bandara:
        filtered_df = filtered_df[filtered_df['ORIGIN AIRPORT'].isin(selected_bandara)]

    fig = px.histogram(filtered_df, x='AIRLINE', color='AIRLINE', title='Jumlah Penerbangan per Maskapai')
    return fig, filtered_df.to_dict("records")

# Run
if __name__ == '__main__':
    app.run_server(debug=True)
