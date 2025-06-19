import streamlit as st # Importa a biblioteca Streamlit, usada para criar a interface web
import pandas as pd # Importa o pandas, usado para manipular os dados em formato de tabela (DataFrame)
import altair as alt # Importa o Altair, biblioteca para criar gráficos interativos

# Define o título da página exibido no topo da interface
st.title("Ranking dos Números Mais Sorteados da Mega-Sena")

# Cria um componente que permite o upload de um arquivo CSV pelo usuário
arquivo = st.file_uploader("Envie o arquivo .csv com os resultados da Mega-Sena", type=["csv"])
    
# Verifica se o usuário enviou algum arquivo
if arquivo is not None:
    df = pd.read_csv(arquivo)# Lê o conteúdo do arquivo CSV em um DataFrame do pandas
    if "Dezenas" in df.columns:# Verifica se existe a coluna "Dezenas" no DataFrame

        # Converte a string de dezenas separadas por vírgulas em listas de inteiros
        df["Dezenas_lista"] = df["Dezenas"].apply(lambda x: [int(n.strip()) for n in x.split(",")])
        # Junta todas as dezenas de todos os sorteios em uma única lista
        todas_dezenas = [dezena for sublist in df["Dezenas_lista"] for dezena in sublist]
        # Conta a frequência de cada número sorteado e ordena do mais frequente para o menos
        freq = pd.Series(todas_dezenas).value_counts().sort_values(ascending=False)
        # Garante que todos os 60 números da Mega-Sena estejam presentes na contagem
        for i in range(1, 61):
            if i not in freq:
                freq[i] = 0
        # Reordena novamente após adicionar os ausentes
        freq = freq.sort_values(ascending=False)
        # Calcula o total de sorteios realizados
        total_sorteios = len(df)
        # Como cada sorteio tem 6 dezenas, calcula o total de dezenas sorteadas
        total_dezenas = total_sorteios * 6
        # Cria um novo DataFrame com os números, frequência absoluta e percentual
        df_freq = pd.DataFrame({
            "Número": freq.index.astype(int),  # Número sorteado
            "Frequência": freq.values,         # Quantidade de vezes que apareceu
            "%": (freq.values / total_dezenas * 100).round(2)  # Porcentagem
        })
        # Cria um gráfico de barras horizontais com Altair
        chart_freq = alt.Chart(df_freq).mark_bar().encode(x=alt.X("%:Q", axis=alt.Axis(format=".2f"),
                    title="Percentual de Vezes Sorteado"), # Titulo 
                    y=alt.Y("Número:O", sort='-x'),  # Ordena do mais ao menos sorteado
                    color=alt.value("#2ecc71")).properties(height=800) # Cor verde e Altura do gráfico
    
        # Adiciona os valores numéricos ao lado das barras no gráfico
        text_freq = alt.Chart(df_freq).mark_text(align='left', dx=3).encode(
            x=alt.X("%:Q", axis=None),
            y=alt.Y("Número:O", sort='-x'),
            text=alt.Text("%:Q", format=".2f"))
        
        # Exibe o gráfico (barras + textos) na interface
        st.altair_chart(chart_freq + text_freq, use_container_width=True)

        # Função que gera uma barra de progresso visual em HTML para cada número
        def make_bar_html(value):
            percent = f"{value:.2f}%"
            bar = f"""
                <div style='background-color:#f0f0f0; width:100%; height:18px; border-radius:4px;'>
                    <div style='background-color:#2ecc71; width:{value}%; height:100%; border-radius:4px;'></div>
                </div>
                <small>{percent}</small>
            """
            return bar

        # Cria uma nova coluna com as barras HTML personalizadas
        df_freq["Visual"] = df_freq["%"].apply(make_bar_html)

        # Estiliza a tabela HTML para alinhar verticalmente as células
        st.markdown(
            "<style>td {vertical-align: middle;}</style>", unsafe_allow_html=True)

        # Exibe cada número com sua frequência e barra de visualização
        for _, row in df_freq.iterrows():
            st.markdown(
                f"**Número {int(row['Número']):02d}** — {int(row['Frequência'])} vezes",
                unsafe_allow_html=True
            )
            st.markdown(row["Visual"], unsafe_allow_html=True)

    else:
        # Exibe aviso caso a coluna "Dezenas" não esteja presente no arquivo
        st.warning(
            "O arquivo precisa ter a coluna 'Dezenas' com os números separados por vírgula.")
else:
    # Informa que o sistema está aguardando o envio de arquivo
    st.info("Aguardando o envio do arquivo .csv...")