import pandas as pd
from dash import Dash, html

# Caminho do CSV no GitHub
URL_CSV = "https://raw.githubusercontent.com/MarcosMoreiraRJ/megasena/main/resultados_megasena.csv"

# Carrega os dados
df = pd.read_csv(URL_CSV)

# Função para criar barra HTML visual
def make_bar_html(value, total):
    percent = (value / total * 100) if total > 0 else 0
    return html.Div([
        html.Div(style={
            'background-color': '#f0f0f0',
            'width': '100%',
            'height': '18px',
            'border-radius': '4px',
            'margin-bottom': '2px',
            'position': 'relative'
        }, children=[
            html.Div(style={
                'background-color': '#2ecc71',
                'width': f'{percent}%',
                'height': '100%',
                'border-radius': '4px'
            })
        ]),
        html.Small(f"{percent:.2f}%")
    ])

# Processamento se a coluna Dezenas existir
if "Dezenas" in df.columns:
    df["Dezenas_lista"] = df["Dezenas"].apply(lambda x: [int(n.strip()) for n in x.split(",")])

    # Inicializa contadores por posição (1 a 6), cada um com 6 linhas
    posicoes = {i: [0]*6 for i in range(1, 7)}

    for dezenas in df["Dezenas_lista"]:
        for i, numero in enumerate(dezenas):
            linha = (numero - 1) // 10  # Linha de 0 a 5
            posicoes[i + 1][linha] += 1

    total_sorteios = len(df)

    # Cria o layout das 6 colunas
    colunas_layout = []
    for posicao in range(1, 7):
        conteudo_coluna = [html.H4(f"Número {posicao}")]
        for linha_idx, valor in enumerate(posicoes[posicao]):
            conteudo_coluna.append(html.Strong(f"Linha {linha_idx + 1} — {valor} sorteios"))
            conteudo_coluna.append(make_bar_html(valor, total_sorteios))
        colunas_layout.append(html.Div(conteudo_coluna, style={"width": "16%", "display": "inline-block", "vertical-align": "top", "padding": "10px"}))
else:
    colunas_layout = [html.Div("O arquivo precisa ter a coluna 'Dezenas'.", style={"color": "red"})]

# Cria o app
app = Dash(__name__)
app.title = "Distribuição por Linhas nas Posições - Mega-Sena"

# Layout final
app.layout = html.Div([
    html.Div(colunas_layout, style={"display": "flex", "justifyContent": "space-between", "flexWrap": "nowrap", "fontFamily": "sans-serif"})
], style={"padding": "5px"})

# Executa
if __name__ == "__main__":
    app.run(debug=True)