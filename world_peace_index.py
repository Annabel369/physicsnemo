# Arquivo: world_peace_index.py
#
# Aplicação Streamlit para visualizar um Índice de Paz Simulada (Peace Index Score)
# dividido em 9 grandes regiões globais.
#
# Pré-requisitos:
# pip install streamlit pandas altair numpy

import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from urllib.error import URLError

# --- Configuração e Cache de Dados ---

# Lista das 9 grandes regiões globais (baseado em divisões comuns para relatórios)
GLOBAL_REGIONS = [
    "América do Norte",
    "América Latina e Caribe",
    "Europa Ocidental",
    "Europa Oriental e Ásia Central",
    "Oriente Médio e Norte da África (MENA)",
    "África Subsaariana",
    "Sul da Ásia",
    "Leste da Ásia e Pacífico",
    "Oceania",
]

@st.cache_data
def get_peace_index_data() -> pd.DataFrame:
    """
    Simula dados de um 'Índice de Paz' (Peace Index Score) ao longo de 3 anos.
    Um *valor mais baixo* representa um índice de paz *mais alto* (mais pacífico).
    """
    st.info("Simulando dados de Índice de Paz. Os dados são fictícios.")

    # Cria dados simulados para 2020, 2021, 2022
    years = [2020, 2021, 2022]
    data = {}

    # Gera pontuações aleatórias para cada região e ano.
    # Usamos np.random.normal para simular uma distribuição mais realista,
    # com pontuações médias diferentes para cada região (simulando diferenças reais).
    np.random.seed(42) # Semente para garantir dados consistentes

    for region in GLOBAL_REGIONS:
        # Define uma pontuação base para a região (simulando paz inerente)
        base_score = np.random.uniform(1.0, 3.5)
        # Gera 3 anos de dados com pequenas variações
        scores = np.clip(np.random.normal(base_score, 0.2, len(years)), 1.0, 4.0)
        data[region] = scores.round(2)

    df = pd.DataFrame(data, index=years)
    df.index.name = "Ano"
    return df.T.rename(columns=str) # Transpõe e garante que os anos são strings para Altair

# --- Layout do Streamlit ---

st.set_page_config(page_title="Índice de Paz Global", layout="wide")

st.title("🕊️ Índice de Paz Global (Simulado)")
st.caption("Comparação do Índice de Paz (Peace Index Score) entre 9 regiões do mundo.")
st.markdown("---")


try:
    df = get_peace_index_data()

    # Seletor de Múltiplas Regiões
    regions = st.multiselect(
        "Escolha as regiões para comparar", 
        list(df.index), 
        # Seleciona algumas regiões por padrão
        ["Europa Ocidental", "América Latina e Caribe", "Oriente Médio e Norte da África (MENA)"]
    )

    if not regions:
        st.error("Por favor, selecione pelo menos uma região para visualizar.")
    else:
        data = df.loc[regions]
        
        # Tabela de Dados (Score: 1.0 = Mais Pacífica, 4.0 = Menos Pacífica)
        st.subheader("Tabela de Pontuações de Paz (Score)")
        st.dataframe(data.sort_index().style.background_gradient(cmap='RdYlGn_r'), use_container_width=True) # RdYlGn_r inverte o gradiente para que verde (Green) seja baixo (mais paz)
        st.markdown("*Nota: Pontuações mais baixas (próximas de 1.0) representam maior paz.*")

        # --- Preparação dos Dados para Altair ---
        # Transforma os dados de colunas largas para longas
        data_long = data.T.reset_index().rename(columns={"index": "Ano"})
        data_long = pd.melt(
            data_long,
            id_vars=["Ano"],
            var_name="Região",
            value_name="Peace Index Score"
        )
        
        # Converte a coluna Ano para tipo temporal (T) para garantir a ordenação correta no gráfico
        data_long["Ano"] = pd.to_datetime(data_long["Ano"], format="%Y")
        
        st.markdown("---")
        st.subheader("Visualização da Evolução do Índice de Paz")
        
        # --- Criação do Gráfico Altair ---
        
        chart = (
            alt.Chart(data_long)
            .mark_area(opacity=0.6, line=True)
            .encode(
                # Eixo X: Ano (Temporal)
                x=alt.X("Ano:T", axis=alt.Axis(format="%Y")),
                # Eixo Y: Score (Quantitativo), permitindo sobreposição (stack=None)
                y=alt.Y("Peace Index Score:Q", 
                        stack=None,
                        scale=alt.Scale(domain=[1.0, 4.0]) # Fixa a escala
                ),
                # Cor: Região (Nominal)
                color="Região:N",
                # Tooltip para exibir detalhes ao passar o mouse
                tooltip=["Ano:T", "Região:N", "Peace Index Score:Q"]
            ).properties(
                title="Evolução do Índice de Paz (Score por Ano)"
            ).interactive() # Permite zoom e pan
        )
        
        st.altair_chart(chart, use_container_width=True)

except URLError as e:
    st.error(f"Este demo requer acesso à internet para carregar o Streamlit e bibliotecas. Erro de Conexão: {e.reason}")
    st.stop()
except Exception as e:
    st.error(f"Ocorreu um erro: {e}")