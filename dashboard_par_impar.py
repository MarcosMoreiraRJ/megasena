import streamlit as st # Importa o módulo Streamlit para criar interfaces web interativas
import pandas as pd # Importa a biblioteca pandas para manipulação de dados em tabelas (DataFrames)
import altair as alt # Importa a biblioteca Altair para visualizações de dados (gráficos)

# Função para calcular quantas colunas diferentes os números ocupam no volante da Mega-Sena
def calcular_colunas(numeros):
    colunas = set()  # Cria um conjunto vazio para armazenar colunas únicas
    for numero in numeros:
        numero = int(numero)  # Garante que cada número é inteiro
        coluna = (numero - 1) % 6 + 1  # Calcula em qual coluna do volante ele estaria
        colunas.add(coluna)  # Adiciona ao conjunto
    return len(colunas)  # Retorna o total de colunas únicas

# Função para contar quantos números pares e ímpares há em um sorteio
def contar_pares_impares(numeros):
    pares = sum(1 for n in numeros if n % 2 == 0)  # Conta os pares
    impares = 6 - pares  # Como são sempre 6 dezenas, os ímpares são o restante
    return f"{pares} Números Pares - {impares} Números Impares"  # Retorna string formatada

# Permite que o usuário envie um arquivo CSV contendo os resultados da Mega-Sena
arquivo = st.file_uploader(
    "Envie o arquivo .csv com os resultados da Mega-Sena", type=["csv"])

# Se um arquivo for enviado
if arquivo is not None:
    
    df = pd.read_csv(arquivo) # Lê o arquivo CSV em um DataFrame do pandas
    # Verifica se existe uma coluna chamada "Dezenas"
    if "Dezenas" in df.columns:
        # Converte a string de dezenas em uma lista de inteiros para cada linha
        df["Dezenas_lista"] = df["Dezenas"].apply(lambda x: [int(n.strip()) for n in x.split(",")])
            
        # -------- ANÁLISE DE PAR/ÍMPAR --------

        st.subheader("Distribuição de Números Pares e Ímpares") # Exibe o título da seção

        
        df["Paridade"] = df["Dezenas_lista"].apply(contar_pares_impares) # Aplica a função que conta pares/ímpares para cada sorteio
        contagem_paridade = df["Paridade"].value_counts().sort_index() # Conta quantas vezes cada distribuição par/ímpar aparece
        total_par = contagem_paridade.sum() # Soma total de sorteios para cálculo de porcentagens

        # Cria um novo DataFrame com as informações formatadas para o gráfico
        df_paridade = pd.DataFrame({
            "Distribuição Par/Ímpar": contagem_paridade.index,
            "Sorteios": contagem_paridade.values,
            "%": (contagem_paridade.values / total_par * 100).round(2)}) # Calcula porcentagem
        
        # Cria o gráfico de barras usando Altair
        chart_par = alt.Chart(df_paridade).mark_bar().encode(
            x=alt.X("%:Q", axis=alt.Axis(format=".2f")),  # Eixo X é a porcentagem
            y=alt.Y("Distribuição Par/Ímpar:N", sort=alt.EncodingSortField(field="Distribuição Par/Ímpar", order="ascending")),  # Ordena o eixo Y   
            color=alt.value("#2ecc71")).properties(height=300)  # Cor e Altura do gráfico
        
        # Adiciona texto com o valor da porcentagem sobre as barras
        text_par = alt.Chart(df_paridade).mark_text(align='left', dx=3).encode(
            x=alt.X("%:Q", axis=None),  # Eixo X não exibe linha
            y=alt.Y("Distribuição Par/Ímpar:N", sort=alt.EncodingSortField(field="Distribuição Par/Ímpar", order="ascending")),
            text=alt.Text("%:Q", format=".2f"))  # Formata o texto como porcentagem

        # Exibe o gráfico com o texto no Streamlit
        st.altair_chart(chart_par + text_par, use_container_width=True)

        # -------- CRIAÇÃO DE BARRA VISUAL HTML --------

        # Função que gera uma barra visual em HTML com base na porcentagem
        def make_bar_html(value):
            percent = f"{value:.2f}%"  # Converte valor para string com %
            bar = f"""
                <div style='background-color:#f0f0f0; width:100%; height:18px; border-radius:4px;'>
                    <div style='background-color:#2ecc71; width:{value}%; height:100%; border-radius:4px;'></div>
                </div>
                <small>{percent}</small>
            """
            return bar  # Retorna o HTML completo

        df_paridade["Visual"] = df_paridade["%"].apply(make_bar_html) # Aplica essa função na coluna de porcentagem

        # Ajuste de estilo para melhorar visualização
        st.markdown("<style>td {vertical-align: middle;}</style>", unsafe_allow_html=True)
            
        # Para cada linha da tabela, mostra o nome da distribuição e a barra visual
        for _, row in df_paridade.iterrows():
            st.markdown(
                f"**{row['Distribuição Par/Ímpar']}** — {int(row['Sorteios'])} sorteios",unsafe_allow_html=True)
                
            st.markdown(row["Visual"], unsafe_allow_html=True)

    # Se não tiver a coluna "Dezenas", avisa o usuário
    else:
        st.warning(
            "O arquivo precisa ter a coluna 'Dezenas' com os números separados por vírgula.")
# Se nenhum arquivo foi enviado, mostra mensagem de informação
else:
    st.info("Aguardando o envio do arquivo .csv...")