import streamlit as st  # Interface web interativa
import pandas as pd     # Manipulação de dados em tabelas
import altair as alt    # Geração de gráficos

# Caminho fixo para o arquivo CSV
arquivo = "https://raw.githubusercontent.com/MarcosMoreiraRJ/megasena/main/resultados_megasena.csv"

try:
    # Carrega o CSV diretamente do disco
    df = pd.read_csv(arquivo)

    if "Dezenas" in df.columns:
        df["Dezenas_lista"] = df["Dezenas"].apply(lambda x: [int(n.strip()) for n in x.split(",")])
        df["Soma"] = df["Dezenas_lista"].apply(sum)

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

        df["Faixa_Soma"] = df["Soma"].apply(classificar_soma)
        contagem = df["Faixa_Soma"].value_counts().sort_index()

        faixas = ["21 a 75", "76 a 129", "130 a 183", "184 a 237", "238 a 291", "292 a 345"]
        for faixa in faixas:
            if faixa not in contagem:
                contagem[faixa] = 0
        contagem = contagem[faixas]

        total = contagem.sum()
        df_contagem = pd.DataFrame({
            "Faixa de Soma": contagem.index,
            "Sorteios": contagem.values,
            "%": (contagem.values / total * 100).round(2)
        })

        def make_bar_html(value):
            percent = f"{value:.2f}%"
            return f"""
                <div style='background-color:#f0f0f0; width:100%; height:18px; border-radius:4px;'>
                    <div style='background-color:#2ecc71; width:{value}%; height:100%; border-radius:4px;'></div>
                </div>
                <small>{percent}</small>
            """

        df_contagem["Visual"] = df_contagem["%"].apply(make_bar_html)

        st.markdown("<style>td {{vertical-align: middle;}}</style>", unsafe_allow_html=True)

        for _, row in df_contagem.iterrows():
            st.markdown(
                f"**Faixa {row['Faixa de Soma']}** — {int(row['Sorteios'])} sorteios",
                unsafe_allow_html=True
            )
            st.markdown(row["Visual"], unsafe_allow_html=True)

    else:
        st.warning("O arquivo precisa ter a coluna 'Dezenas' com os números separados por vírgula.")

except FileNotFoundError:
    st.error(f"Arquivo não encontrado no caminho:\n{arquivo}")
except Exception as e:
    st.error(f"Ocorreu um erro ao carregar o arquivo:\n{e}")