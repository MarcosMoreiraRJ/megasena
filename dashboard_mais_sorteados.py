import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px


# URL do CSV diretamente do GitHub (RAW)
URL_CSV = "https://raw.githubusercontent.com/MarcosMoreiraRJ/megasena/main/resultados_megasena.csv"

# Carrega o DataFrame
df = pd.read_csv(URL_CSV)

# Processa os dados se a coluna "Dezenas" existir
if "Dezenas" in df.columns:
    df["Dezenas_lista"] = df["Dezenas"].apply(lambda x: [int(n.strip()) for n in x.split(",")])
    todas_dezenas = [dezena for dezenas in df["Dezenas_lista"] for dezena in dezenas]
    freq = pd.Series(todas_dezenas).value_counts().sort_values(ascending=False)

    # Garante todos os números de 1 a 60
    for i in range(1, 61):
        if i not in freq:
            freq[i] = 0

    freq = freq.sort_values(ascending=False)
    total_sorteios = len(df)
    total_dezenas = total_sorteios * 6

    df_freq = pd.DataFrame({
        "Número": freq.index.astype(int),
        "Frequência": freq.values,
        "%": (freq.values / total_dezenas * 100).round(2)
    })

else:
    df_freq = pd.DataFrame(columns=["Número", "Frequência", "%"])

# Gráfico com Plotly
fig = px.bar(
    df_freq,
    x="%",
    y="Número",
    orientation="h",
    text="%",
    color_discrete_sequence=["#2ecc71"]
)
fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
fig.update_layout(height=900, margin=dict(l=20, r=20, t=40, b=40))

# Função para criar barra HTML
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

# Inicializa o app Dash
app = Dash(__name__)
app.title = "Ranking de Números Mais Sorteados - Mega-Sena"

# Layout do app
app.layout = html.Div([
    
    html.Div([
        html.Div([
            html.Strong(f"Número {int(row['Número']):02d} — {int(row['Frequência'])} vezes"),
            make_bar_html(row["%"])
        ], style={"marginBottom": "16px"})
        for _, row in df_freq.iterrows()
    ])
], style={"padding": "30px", "fontFamily": "sans-serif"})

# Roda o servidor
if __name__ == "__main__":
    app.run(debug=True)

