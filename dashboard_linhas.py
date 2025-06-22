import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# Caminho direto para o CSV hospedado no GitHub
URL_CSV = "https://raw.githubusercontent.com/MarcosMoreiraRJ/megasena/main/resultados_megasena.csv"

# Função que calcula quantas linhas diferentes os números ocupam na cartela da Mega-Sena
def calcular_linhas(numeros):
    linhas = set()
    for numero in numeros:
        numero = int(numero)
        linha = (numero - 1) // 10 + 1
        linhas.add(linha)
    return len(linhas)

# Carrega os dados do GitHub
df = pd.read_csv(URL_CSV)

# Processamento dos dados
if "Dezenas" in df.columns:
    df["Dezenas_lista"] = df["Dezenas"].apply(lambda x: [int(n.strip()) for n in x.split(",")])
    df["Linhas_ocupadas"] = df["Dezenas_lista"].apply(calcular_linhas)
    contagem = df["Linhas_ocupadas"].value_counts().sort_index()

    for i in range(1, 7):
        if i not in contagem:
            contagem[i] = 0

    contagem = contagem.sort_index()
    total = contagem.sum()

    df_contagem = pd.DataFrame({
        "Linhas Ocupadas": contagem.index,
        "Sorteios": contagem.values,
        "%": (contagem.values / total * 100).round(2)
    })
else:
    df_contagem = pd.DataFrame(columns=["Linhas Ocupadas", "Sorteios", "%"])

# Gráfico com Plotly
fig = px.bar(
    df_contagem,
    x="%",
    y="Linhas Ocupadas",
    orientation="h",
    text="%",
    color_discrete_sequence=["#2ecc71"]
)
fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=40))

# Função para gerar barras HTML
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
app.title = "Distribuição por Linhas - Mega-Sena"

# Layout da página
app.layout = html.Div([

    html.Div([
        html.Div([
            html.Strong(f"{int(row['Linhas Ocupadas'])} Linhas Ocupadas — {int(row['Sorteios'])} sorteios"),
            make_bar_html(row["%"])
        ], style={"marginBottom": "16px"})
        for _, row in df_contagem.iterrows()
    ])
], style={"padding": "30px", "fontFamily": "sans-serif"})

# Executa o servidor
if __name__ == "__main__":
    app.run(debug=True)