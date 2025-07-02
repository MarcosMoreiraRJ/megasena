from flask import Flask, render_template_string
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

# Importa os apps Dash de cada arquivo
from dashboard_colunas import app as dash_colunas
from dashboard_linhas import app as dash_linhas
from dashboard_mais_sorteados import app as dash_mais
from dashboard_par_impar import app as dash_par
from dashboard_posicao import app as dash_posicao
from dashboard_somas import app as dash_somas

# Cria o app Flask principal
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    html = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
      <meta charset="UTF-8" />
      <title>Dashboard Mega-Sena Interativo</title>
      <script src="https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/Sortable.min.js"></script>
      <style>
        body {
          font-family: sans-serif;
          margin: 0;
          padding: 20px;
          background-color: #f9f9f9;
        }
        .grid-container {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 20px;
        }
        .card {
          background-color: white;
          border: 1px solid #ccc;
          border-radius: 8px;
          box-shadow: 0 2px 6px rgba(0,0,0,0.1);
          padding: 16px;
          cursor: move;
        }
        .card h2 {
          margin-top: 0;
        }
        iframe {
          width: 100%;
          height: 100%;
          border: none;
        }
      </style>
    </head>
    <body>
      <h1> Dashboards Mega-Sena </h1>
      <div class="grid-container" id="dash-container">
        <div class="card">
          <h2>Número de Colunas</h2>
          <iframe src="/colunas/"></iframe>
        </div>
        <div class="card">
          <h2>Número de Linhas</h2>
          <iframe src="/linhas/"></iframe>
        </div>
        <div class="card">
          <h2>Proporção de Par ou Ímpar</h2>
          <iframe src="/parimparposicao/"></iframe>
        </div>
        <div class="card">
          <h2>Soma dos Números Sorteados</h2>
          <iframe src="/somas/"></iframe>
        </div>
        <div class="card">
          <h2>Proporção de cada Número</h2>
          <iframe src="/posicao/"></iframe>
        </div>
        <div class="card">
          <h2>Números mais Sorteados</h2>
          <iframe src="/mais_sorteados/"></iframe>
        </div>
      </div>

      <script>
        new Sortable(document.getElementById("dash-container"), {
          animation: 150,
          ghostClass: 'blue-background-class'
        });
      </script>
    </body>
    </html>
    """
    return render_template_string(html)

# Usa DispatcherMiddleware para combinar Flask com múltiplos apps Dash
application = DispatcherMiddleware(flask_app, {
    "/colunas": dash_colunas.server,
    "/linhas": dash_linhas.server,
    "/mais_sorteados": dash_mais.server,
    "/parimpar": dash_par.server,
    "/posicao": dash_posicao.server,
    "/somas": dash_somas.server
})

if __name__ == "__main__":
    run_simple("localhost", 8050, application, use_reloader=True, use_debugger=True)