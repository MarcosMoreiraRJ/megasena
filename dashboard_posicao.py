import streamlit as st
import pandas as pd

# Upload do arquivo
arquivo = "https://raw.githubusercontent.com/MarcosMoreiraRJ/megasena/main/resultados_megasena.csv"

# Se houver arquivo
if arquivo is not None:
    df = pd.read_csv(arquivo)

    if "Dezenas" in df.columns:
        # Converte a string em lista de inteiros
        df["Dezenas_lista"] = df["Dezenas"].apply(lambda x: [int(n.strip()) for n in x.split(",")])

        # Inicializa um dicionário para cada posição
        posicoes = {
            1: [0]*6,
            2: [0]*6,
            3: [0]*6,
            4: [0]*6,
            5: [0]*6,
            6: [0]*6
        }

        # Conta as ocorrências de linha por posição
        for dezenas in df["Dezenas_lista"]:
            for i, numero in enumerate(dezenas):
                linha = (numero - 1) // 10  # linha de 0 a 5
                posicoes[i + 1][linha] += 1

        # Layout com 6 colunas (uma para cada número)
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        colunas = [col1, col2, col3, col4, col5, col6]

        total_sorteios = len(df)

        # Função para criar barra HTML
        def make_bar_html(value, total):
            percent = (value / total * 100) if total > 0 else 0
            bar = f"""
                <div style='background-color:#f0f0f0; width:100%; height:18px; border-radius:4px; margin-bottom:2px;'>
                    <div style='background-color:#2ecc71; width:{percent}%; height:100%; border-radius:4px;'></div>
                </div>
                <small>{percent:.2f}%</small>
            """
            return bar

        # Preenche cada coluna com os dados de barra
        for idx, col in enumerate(colunas):
            pos = idx + 1
            col.markdown(f"### Número{pos}")
            for i, count in enumerate(posicoes[pos]):
                col.markdown(f"**Linha {i + 1}** — {count} sorteios", unsafe_allow_html=True)
                col.markdown(make_bar_html(count, total_sorteios), unsafe_allow_html=True)

    else:
        st.warning("O arquivo precisa ter a coluna 'Dezenas' com os números separados por vírgula.")
else:
    st.info("Aguardando o envio do arquivo .csv...")