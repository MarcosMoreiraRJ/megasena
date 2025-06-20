import streamlit as st
import pandas as pd
import altair as alt

# Caminho direto para o arquivo CSV no GitHub (link RAW)
arquivo = "https://raw.githubusercontent.com/MarcosMoreiraRJ/megasena/main/resultados_megasena.csv"

# Função que calcula quantas colunas diferentes os números ocupam no volante da Mega-Sena
def calcular_colunas(numeros):
    colunas = set()
    for numero in numeros:
        numero = int(numero)
        coluna = (numero - 1) % 6 + 1
        colunas.add(coluna)
    return len(colunas)

try:
    # Lê diretamente o CSV do GitHub
    df = pd.read_csv(arquivo)

    if "Dezenas" in df.columns:
        df["Dezenas_lista"] = df["Dezenas"].apply(lambda x: [int(n.strip()) for n in x.split(",")])
        df["Colunas_Sorteadas"] = df["Dezenas_lista"].apply(calcular_colunas)
        contagem = df["Colunas_Sorteadas"].value_counts().sort_index()

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

        st.subheader("Distribuição dos Números por Quantidade de Colunas")

        chart = alt.Chart(df_contagem).mark_bar().encode(
            x=alt.X("%:Q", axis=alt.Axis(format=".2f")),
            y=alt.Y("Colunas Sorteadas:N", sort=alt.EncodingSortField(
                field="Colunas Sorteadas", order="ascending")),
            color=alt.value("#2ecc71")
        ).properties(height=300)

        text = alt.Chart(df_contagem).mark_text(align='left', dx=3).encode(
            x=alt.X("%:Q", axis=None),
            y=alt.Y("Colunas Sorteadas:N", sort=alt.EncodingSortField(
                field="Colunas Sorteadas", order="ascending")),
            text=alt.Text("%:Q", format=".2f")
        )

        st.altair_chart(chart + text, use_container_width=True)

        def make_bar_html(value):
            percent = f"{value:.2f}%"
            return f"""
                <div style='background-color:#f0f0f0; width:100%; height:18px; border-radius:4px;'>
                    <div style='background-color:#2ecc71; width:{value}%; height:100%; border-radius:4px;'></div>
                </div>
                <small>{percent}</small>
            """

        df_contagem["Visual"] = df_contagem["%"].apply(make_bar_html)

        st.markdown("<style>td {vertical-align: middle;}</style>", unsafe_allow_html=True)
        for _, row in df_contagem.iterrows():
            st.markdown(f"**{int(row['Colunas Sorteadas'])} Colunas Sorteadas** — {int(row['Sorteios'])} sorteios", unsafe_allow_html=True)
            st.markdown(row["Visual"], unsafe_allow_html=True)

    else:
        st.warning("O arquivo não contém a coluna 'Dezenas'.")

except FileNotFoundError:
    st.error(f"Arquivo não encontrado no caminho:\n{arquivo}")
except Exception as e:
    st.error(f"Ocorreu um erro ao processar o arquivo:\n{e}")