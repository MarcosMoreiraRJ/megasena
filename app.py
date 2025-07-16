# app.py unificado com todos os dashboards incorporados diretamente

from flask import Flask, render_template_string
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

# === Funcoes de utilidade ===

def make_bar_html(value):
    percent = f"{value:.2f}%"
    return html.Div([
        html.Div(style={
            'background-color': '#f0f0f0',
            'width': '100%',
            'height': '20px',
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

URL_CSV = "https://raw.githubusercontent.com/MarcosMoreiraRJ/megasena/main/resultados_megasena.csv"
df = pd.read_csv(URL_CSV)

# === Dash: Colunas ===

def create_colunas_app():
    def calcular_colunas(numeros):
        return len(set((int(n) - 1) % 6 + 1 for n in numeros))

    df_temp = df.copy()
    df_temp["Dezenas_lista"] = df_temp["Dezenas"].apply(lambda x: [int(n.strip()) for n in x.split(",")])
    df_temp["Colunas_Sorteadas"] = df_temp["Dezenas_lista"].apply(calcular_colunas)
    contagem = df_temp["Colunas_Sorteadas"].value_counts().sort_index()
    for i in range(1, 7): contagem[i] = contagem.get(i, 0)
    contagem = contagem.sort_index()
    total = contagem.sum()
    df_contagem = pd.DataFrame({
        "Colunas Sorteadas": contagem.index,
        "Sorteios": contagem.values,
        "%": (contagem.values / total * 100).round(2)
    })
    app = Dash(__name__, requests_pathname_prefix="/colunas/")
    app.layout = html.Div([
        html.Div([
            html.Div([
                html.Strong(f"{int(row['Colunas Sorteadas'])} Colunas Sorteadas — {int(row['Sorteios'])} sorteios"),
                make_bar_html(row["%"])
            ], style={"marginBottom": "16px"})
            for _, row in df_contagem.iterrows()
        ])
    ], style={"padding": "30px", "fontFamily": "sans-serif"})
    return app

# === Dash: Linhas ===

def create_linhas_app():
    def calcular_linhas(numeros):
        return len(set((int(n) - 1) // 10 + 1 for n in numeros))

    df_temp = df.copy()
    df_temp["Dezenas_lista"] = df_temp["Dezenas"].apply(lambda x: [int(n.strip()) for n in x.split(",")])
    df_temp["Linhas_ocupadas"] = df_temp["Dezenas_lista"].apply(calcular_linhas)
    contagem = df_temp["Linhas_ocupadas"].value_counts().sort_index()
    for i in range(1, 7): contagem[i] = contagem.get(i, 0)
    contagem = contagem.sort_index()
    total = contagem.sum()
    df_contagem = pd.DataFrame({
        "Linhas Ocupadas": contagem.index,
        "Sorteios": contagem.values,
        "%": (contagem.values / total * 100).round(2)
    })
    app = Dash(__name__, requests_pathname_prefix="/linhas/")
    app.layout = html.Div([
        html.Div([
            html.Div([
                html.Strong(f"{int(row['Linhas Ocupadas'])} Linhas Ocupadas — {int(row['Sorteios'])} sorteios"),
                make_bar_html(row["%"])
            ], style={"marginBottom": "16px"})
            for _, row in df_contagem.iterrows()
        ])
    ], style={"padding": "30px", "fontFamily": "sans-serif"})
    return app

# === Dash: Mais Sorteados ===

def create_mais_sorteados_app():
    df_temp = df.copy()
    df_temp["Dezenas_lista"] = df_temp["Dezenas"].apply(lambda x: [int(n.strip()) for n in x.split(",")])
    todas_dezenas = [dezena for dezenas in df_temp["Dezenas_lista"] for dezena in dezenas]
    freq = pd.Series(todas_dezenas).value_counts().sort_values(ascending=False)
    for i in range(1, 61): freq[i] = freq.get(i, 0)
    freq = freq.sort_values(ascending=False)
    total_sorteios = len(df_temp)
    total_dezenas = total_sorteios * 6
    df_freq = pd.DataFrame({
        "Número": freq.index.astype(int),
        "Frequência": freq.values,
        "%": (freq.values / total_dezenas * 100).round(2)
    })
    fig = px.pie(
        df_freq.head(15),
        values="Frequência",
        names="Número",
        title="Top 15 Números Mais Sorteados",
        color_discrete_sequence=["#2ecc71", "#f0f0f0", "#ffffff"] * 5
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=40))
    app = Dash(__name__, requests_pathname_prefix="/mais_sorteados/")
    app.layout = html.Div([
        html.H2("Top 15 Números Mais Sorteados da Mega-Sena", style={"textAlign": "center"}),
        dcc.Graph(figure=fig)
    ], style={"padding": "30px", "fontFamily": "sans-serif"})
    return app

# === Dash: Par ou Ímpar ===

def create_par_impar_app():
    def contar_pares_impares(numeros):
        pares = sum(1 for n in numeros if n % 2 == 0)
        impares = 6 - pares
        return f"{pares} Números Pares - {impares} Números Impares"

    df_temp = df.copy()
    df_temp["Dezenas_lista"] = df_temp["Dezenas"].apply(lambda x: [int(n.strip()) for n in x.split(",")])
    df_temp["Paridade"] = df_temp["Dezenas_lista"].apply(contar_pares_impares)
    contagem = df_temp["Paridade"].value_counts().sort_index()
    total = contagem.sum()
    df_contagem = pd.DataFrame({
        "Distribuição Par/Ímpar": contagem.index,
        "Sorteios": contagem.values,
        "%": (contagem.values / total * 100).round(2)
    })
    app = Dash(__name__, requests_pathname_prefix="/parimpar/")
    app.layout = html.Div([
        html.Div([
            html.Div([
                html.Strong(f"{row['Distribuição Par/Ímpar']} — {int(row['Sorteios'])} sorteios"),
                make_bar_html(row["%"])
            ], style={"marginBottom": "16px"})
            for _, row in df_contagem.iterrows()
        ])
    ], style={"padding": "30px", "fontFamily": "sans-serif"})
    return app

# === Dash: Posicao ===

def create_posicao_app():
    df_temp = df.copy()
    df_temp["Dezenas_lista"] = df_temp["Dezenas"].apply(lambda x: [int(n.strip()) for n in x.split(",")])
    posicoes = {i: [0]*6 for i in range(1, 7)}
    for dezenas in df_temp["Dezenas_lista"]:
        for i, numero in enumerate(dezenas):
            linha = (numero - 1) // 10
            posicoes[i + 1][linha] += 1
    total_sorteios = len(df_temp)

    app = Dash(__name__, requests_pathname_prefix="/posicao/")

    # Layout com posições lado a lado
    layout_horizontal = html.Div([
        html.Div([
            html.Div([
                html.H4(f"Número {pos}", style={"textAlign": "center",}),
                *[
                    html.Div([
                        html.Strong(f"Linha {i + 1} — {count} sorteios"),
                        make_bar_html((count / total_sorteios * 100))
                    ], style={}) for i, count in enumerate(posicoes[pos])
                ]
            ], style={
                "flex": "1",
                "minWidth": "200px",
                "maxWidth": "100%",
                "background": "#fdfdfd",
            })
            for pos in range(1, 7)
        ], style={
            "display": "flex",
            "flexWrap": "nowrap",
            "overflowX": "auto",
            "gap": "12px"
        })
    ], style={"padding": "30px", "fontFamily": "sans-serif"})

    app.layout = layout_horizontal
    return app

# === Dash: Somas ===

def create_somas_app():
    def classificar_soma(soma):
        if 21 <= soma <= 75: return "21 a 75"
        elif 76 <= soma <= 129: return "76 a 129"
        elif 130 <= soma <= 183: return "130 a 183"
        elif 184 <= soma <= 237: return "184 a 237"
        elif 238 <= soma <= 291: return "238 a 291"
        elif 292 <= soma <= 345: return "292 a 345"
        else: return "Fora do intervalo"

    df_temp = df.copy()
    df_temp["Dezenas_lista"] = df_temp["Dezenas"].apply(lambda x: [int(n.strip()) for n in x.split(",")])
    df_temp["Soma"] = df_temp["Dezenas_lista"].apply(sum)
    df_temp["Faixa_Soma"] = df_temp["Soma"].apply(classificar_soma)
    contagem = df_temp["Faixa_Soma"].value_counts().sort_index()
    faixas = ["21 a 75", "76 a 129", "130 a 183", "184 a 237", "238 a 291", "292 a 345"]
    for faixa in faixas: contagem[faixa] = contagem.get(faixa, 0)
    contagem = contagem[faixas]
    total = contagem.sum()
    df_contagem = pd.DataFrame({
        "Faixa de Soma": contagem.index,
        "Sorteios": contagem.values,
        "%": (contagem.values / total * 100).round(2)
    })
    app = Dash(__name__, requests_pathname_prefix="/somas/")
    app.layout = html.Div([
        html.Div([
            html.Div([
                html.Strong(f"Faixa {row['Faixa de Soma']} — {int(row['Sorteios'])} sorteios"),
                make_bar_html(row["%"])
            ], style={"marginBottom": "16px"})
            for _, row in df_contagem.iterrows()
        ])
    ], style={"padding": "30px", "fontFamily": "sans-serif"})
    return app

# === Apps ===

dash_colunas = create_colunas_app()
dash_linhas = create_linhas_app()
dash_mais = create_mais_sorteados_app()
dash_par = create_par_impar_app()
dash_posicao = create_posicao_app()
dash_somas = create_somas_app()

# === Flask ===

flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='UTF-8'>
        <title>Dashboards Mega-Sena</title>
        <style>
            body {
                font-family: sans-serif;
                padding: 30px;
                background: #f9f9f9;
            }
            h1, h2 {
                text-align: center;
            }
            .generator {
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                margin-bottom: 40px;
                border: 1px solid #ccc;
            }
            .generator h2 {
                margin-top: 0;
            }
            .checkbox-group {
                display: flex;
                flex-wrap: wrap;
                gap: 15px;
                margin: 20px 0;
                justify-content: center;
            }
            .checkbox-group label {
                font-weight: bold;
                display: flex;
                align-items: center;
                gap: 5px;
            }
            .generate-btn {
                display: block;
                margin: 0 auto;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                color: white;
                background-color: #2ecc71;
                border: none;
                border-radius: 6px;
                cursor: pointer;
            }
            .generate-btn:hover {
                background-color: #27ae60;
            }
            .result {
                text-align: center;
                font-size: 24px;
                margin-top: 20px;
                font-weight: bold;
            }
            .grid-container {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }
            .card {
                background: #fff;
                border: 1px solid #ccc;
                border-radius: 8px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                padding: 16px;
            }
            .card-wide {
                grid-column: span 2;
            }
            iframe {
                width: 100%;
                height: 620px;
                border: none;
            }
        </style>
    </head>
    <body>
        <h1>Dashboards Mega-Sena</h1>

        <div class="generator">
            <h2>Gerador Inteligente de Números</h2>
            <form id="form-gerador" onsubmit="gerarNumeros(event)">
                <div class="checkbox-group">
                    <label><input type="checkbox" id="chk_colunas" checked>Colunas</label>
                    <label><input type="checkbox" id="chk_linhas" checked>Linhas</label>
                    <label><input type="checkbox" id="chk_parimpar" checked>Par/Ímpar</label>
                    <label><input type="checkbox" id="chk_somas" checked>Somas</label>
                    <label><input type="checkbox" id="chk_posicao" checked>Posição</label>
                </div>
                <button type="submit" class="generate-btn">Gerar Números</button>
            </form>
            <div class="result" id="resultado-gerado">[  ]</div>
        </div>

        <div class="grid-container">
            <div class="card card-wide"><h2>Posição</h2><iframe src="/posicao/"></iframe></div>
            <div class="card"><h2>Número de Colunas</h2><iframe src="/colunas/"></iframe></div>
            <div class="card"><h2>Número de Linhas</h2><iframe src="/linhas/"></iframe></div>
            <div class="card"><h2>Par ou Ímpar</h2><iframe src="/parimpar/"></iframe></div>
            <div class="card"><h2>Somas</h2><iframe src="/somas/"></iframe></div>
            <div class="card card-wide"><h2>Mais Sorteados</h2><iframe src="/mais_sorteados/"></iframe></div>
        </div>

        <script>
            function gerarNumeros(event) {
                event.preventDefault();

                const usarPosicao = document.getElementById("chk_posicao").checked;
                const usarColunas = document.getElementById("chk_colunas").checked;
                const usarLinhas = document.getElementById("chk_linhas").checked;
                const usarParImpar = document.getElementById("chk_parimpar").checked;
                const usarSomas = document.getElementById("chk_somas").checked;

                const criterios = [];
                if (usarPosicao) criterios.push("Posição");
                if (usarColunas) criterios.push("Colunas");
                if (usarLinhas) criterios.push("Linhas");
                if (usarParImpar) criterios.push("Par/Ímpar");
                if (usarSomas) criterios.push("Somas");
                
                // Essa lógica ainda é apenas placeholder para futura integração com backend
                const numerosAleatorios = Array.from({length: 6}, () => Math.floor(Math.random() * 60) + 1)
                    .sort((a, b) => a - b);

                document.getElementById("resultado-gerado").innerText = 
                    "Critérios usados: " + criterios.join(", ") + "\\nNúmeros gerados: " + numerosAleatorios.join(", ");
            }
        </script>
    </body>
    </html>
    """)


application = DispatcherMiddleware(flask_app, {
    "/colunas": dash_colunas.server,
    "/linhas": dash_linhas.server,
    "/mais_sorteados": dash_mais.server,
    "/parimpar": dash_par.server,
    "/posicao": dash_posicao.server,
    "/somas": dash_somas.server,
})

if __name__ == "__main__":
    run_simple("localhost", 8050, application, use_reloader=True, use_debugger=True, threaded=True)