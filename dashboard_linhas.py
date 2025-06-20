import streamlit as st
import pandas as pd
import altair as alt

# Caminho fixo para o arquivo CSV
arquivo = "https://raw.githubusercontent.com/MarcosMoreiraRJ/megasena/main/resultados_megasena.csv"

# Função que calcula quantas linhas diferentes os números ocupam na cartela da Mega-Sena
def calcular_linhas(numeros):
    linhas = set()
    for numero in numeros:
        numero = int(numero)
        linha = (numero - 1) // 10 + 1
        linhas.add(linha)
    return len(linhas)


# Tenta ler o arquivo direto do disco
try:
    df = pd.read_csv(arquivo)

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
            "Linhas ocupadas": contagem.index,
            "Sorteios": contagem.values,
            "%": (contagem.values / total * 100).round(2)
        })

        # Função para barra HTML
        def make_bar_html(value):
            percent = f"{value:.2f}%"
            return f"""
                <div style='background-color:#f0f0f0; width:100%; height:18px; border-radius:4px;'>
                    <div style='background-color:#2ecc71; width:{value}%; height:100%; border-radius:4px;'></div>
                </div>
                <small>{percent}</small>
            """

        df_contagem["Visual"] = df_contagem["%"].apply(make_bar_html)

        st.subheader("Distribuição dos Números por Quantidade de Linhas")
        st.markdown("<style>td {vertical-align: middle;}</style>", unsafe_allow_html=True)

        for _, row in df_contagem.iterrows():
            st.markdown(f"**{int(row['Linhas ocupadas'])} linhas ocupadas** — {int(row['Sorteios'])} sorteios", unsafe_allow_html=True)
            st.markdown(row["Visual"], unsafe_allow_html=True)

    else:
        st.warning("O arquivo não contém a coluna 'Dezenas'.")

except FileNotFoundError:
    st.error(f"Arquivo não encontrado no caminho:\n{arquivo}")
except Exception as e:
    st.error(f"Ocorreu um erro ao carregar o arquivo:\n{e}")
