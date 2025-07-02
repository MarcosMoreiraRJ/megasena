import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# === Fonte dos dados ===
URL_CSV = "https://raw.githubusercontent.com/MarcosMoreiraRJ/megasena/main/resultados_megasena.csv"

# === Funções auxiliares ===
def contar_par_impar(numeros):
    pares = sum(1 for n in numeros if n % 2 == 0)
    impares = 6 - pares
    return f"{pares} Par - {impares} Impar"

def make_bar_html(value):
    percent = f"{value:.2f}%"
    return html.Div([
        html.Div(style={
            'background-color': '#f0f0f0',
            'width': '100%',
            'height': '18px',
            'border-radius': '4px',
            'position': 'relative'
        }, children=[
            html.Div(style={
                'background-color': '#2ecc71',
                'width': f'{value}%',
                'height': '100%',
                'border-radius': '4px'
            })
        ]),
        html.Small(percent)
    ])

# === Carregamento e processamento dos dados ===
df = pd.read_csv(URL_CSV)

if "Dezenas" in df.columns:
    df["Dezenas_lista"] = df["Dezenas"].apply(lambda x: [int(n.strip()) for n in x.split(",")])

    # ----- Distribuição Par/Ímpar -----
    df["Paridade"] = df["Dezenas_lista"].apply(contar_par_impar)
    padroes = ["6 Par - 0 Impar", "5 Par - 1 Impar", "4 Par - 2 Impar", "3 Par - 3 Impar", "2 Par - 4 Impar", "1 Par - 5 Impar", "0 Par - 6 Impar"]
    contagem_paridade = df["Paridade"].value_counts().reindex(padroes, fill_value=0)
    total_paridade = contagem_paridade.sum()

    df_paridade = pd.DataFrame({
        "Distribuição": contagem_paridade.index,
        "Sorteios": contagem_paridade.values,
        "%": (contagem_paridade.values / total_paridade * 100).round(2)
    })
else:
    df_paridade = pd.DataFrame(columns=["Distribuição", "Sorteios", "%"])

# === Gráfico de paridade ===
fig_paridade = px.bar(
    df_paridade,
    x="%",
    y="Distribuição",
    orientation="h",
    text="%",
    color_discrete_sequence=["#2ecc71"]
)
fig_paridade.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
fig_paridade.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=40))

# === App Dash ===
app = Dash(__name__)
app.title = "Paridade Mega-Sena"

# === Layout ===
app.layout = html.Div([

    

    html.Div([
        html.Div([
            html.Strong(f"{row['Distribuição']} — {int(row['Sorteios'])} sorteios"),
            make_bar_html(row["%"])
        ], style={"marginBottom": "16px"})
        for _, row in df_paridade.iterrows()
    ])
], style={"padding": "30px", "fontFamily": "sans-serif"})

# === Execução ===
if __name__ == "__main__":
    app.run(debug=True)