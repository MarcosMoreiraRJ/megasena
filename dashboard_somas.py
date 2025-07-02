import pandas as pd
from dash import Dash, html

# Caminho do CSV no GitHub
URL_CSV = "https://raw.githubusercontent.com/MarcosMoreiraRJ/megasena/main/resultados_megasena.csv"

# Função que classifica a soma das dezenas em faixas
def classificar_soma(soma):
    if 21 <= soma <= 75:
        return "21 a 75"
    elif 76 <= soma <= 129:
        return "76 a 129"
    elif 130 <= soma <= 183:
        return "130 a 183"
    elif 184 <= soma <= 237:
        return "184 a 237"
    elif 238 <= soma <= 291:
        return "238 a 291"
    elif 292 <= soma <= 345:
        return "292 a 345"
    else:
        return "Fora do intervalo"

# Função para gerar barra HTML visual
def make_bar_html(value):
    percent = f"{value:.2f}%"
    return html.Div([
        html.Div(style={
            'background-color': '#f0f0f0',
            'width': '100%',
            'height': '18px',
            'border-radius': '4px',
            'margin-bottom': '4px'
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

# Lê e processa os dados
try:
    df = pd.read_csv(URL_CSV)

    if "Dezenas" in df.columns:
        df["Dezenas_lista"] = df["Dezenas"].apply(lambda x: [int(n.strip()) for n in x.split(",")])
        df["Soma"] = df["Dezenas_lista"].apply(sum)
        df["Faixa_Soma"] = df["Soma"].apply(classificar_soma)

        contagem = df["Faixa_Soma"].value_counts().sort_index()
        faixas_ordenadas = ["21 a 75", "76 a 129", "130 a 183", "184 a 237", "238 a 291", "292 a 345"]
        for faixa in faixas_ordenadas:
            if faixa not in contagem:
                contagem[faixa] = 0
        contagem = contagem[faixas_ordenadas]

        total = contagem.sum()
        df_contagem = pd.DataFrame({
            "Faixa de Soma": contagem.index,
            "Sorteios": contagem.values,
            "%": (contagem.values / total * 100).round(2)
        })

        # Cria os elementos HTML para o dashboard
        layout_visual = []
        for _, row in df_contagem.iterrows():
            layout_visual.append(html.Strong(f"Faixa {row['Faixa de Soma']} — {int(row['Sorteios'])} sorteios"))
            layout_visual.append(make_bar_html(row["%"]))

    else:
        layout_visual = [html.Div("O arquivo precisa ter a coluna 'Dezenas'.", style={"color": "red"})]

except Exception as e:
    layout_visual = [html.Div(f"Ocorreu um erro ao carregar o arquivo: {e}", style={"color": "red"})]

# Cria app Dash
app = Dash(__name__)
app.title = "Faixa da Soma das Dezenas - Mega-Sena"

app.layout = html.Div([
    html.Div(layout_visual, style={"marginTop": "30px", "fontFamily": "sans-serif"})
], style={"padding": "30px"})

# Executa o servidor
if __name__ == "__main__":
    app.run(debug=True)
