import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# Caminho direto para o CSV hospedado no GitHub (formato RAW)
URL_CSV = "https://raw.githubusercontent.com/MarcosMoreiraRJ/megasena/main/resultados_megasena.csv"

# Função que calcula quantas colunas diferentes os números ocupam na cartela da Mega-Sena
def calcular_colunas(numeros):
    colunas = set()
    for numero in numeros:
        numero = int(numero)
        coluna = (numero - 1) % 6 + 1
        colunas.add(coluna)
    return len(colunas)

# Carrega os dados do GitHub
df = pd.read_csv(URL_CSV)

# Processa os dados se a coluna "Dezenas" existir
if "Dezenas" in df.columns:
    df["Dezenas_lista"] = df["Dezenas"].apply(lambda x: [int(n.strip()) for n in x.split(",")])
    df["Colunas_Sorteadas"] = df["Dezenas_lista"].apply(calcular_colunas)
    contagem = df["Colunas_Sorteadas"].value_counts().sort_index()

    # Garante presença de todas as colunas (1 a 6)
    for i in range(1, 7):
        if i not in contagem:
            contagem[i] = 0

    contagem = contagem.sort_index()
    total = contagem.sum()

    df_contagem = pd.DataFrame({
        "Colunas Sorteadas": contagem.index,
        "Sorteios": contagem.values,
        "%": (contagem.values / total * 100).round(2)
    })

else:
    # DataFrame vazio se algo der errado
    df_contagem = pd.DataFrame(columns=["Colunas Sorteadas", "Sorteios", "%"])

# Geração de gráfico com Plotly
fig = px.bar(
    df_contagem,
    x="%",
    y="Colunas Sorteadas",
    orientation="h",
    text="%",
    color_discrete_sequence=["#2ecc71"]
)
fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=40))

# Função que retorna barra de progresso em HTML
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

# Cria o app Dash
app = Dash(__name__)
app.title = "Distribuição por Colunas - Mega-Sena"

# Layout da página
app.layout = html.Div([
   
    html.Div([
        html.Div([
            html.Strong(f"{int(row['Colunas Sorteadas'])} Colunas Sorteadas — {int(row['Sorteios'])} sorteios"),
            make_bar_html(row["%"])
        ], style={"marginBottom": "16px"})
        for _, row in df_contagem.iterrows()
    ])
], style={"padding": "30px", "fontFamily": "sans-serif"})

# Roda o servidor Dash
if __name__ == "__main__":
    app.run(debug=True, port=8051)