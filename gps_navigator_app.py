# Arquivo: gps_navigator_app.py
#
# Aplicação Streamlit de Navegação GPS (Simulada) usando Pydeck.
# Permite definir um ponto de origem e um ponto de destino no mapa.
#
# Pré-requisitos (Instalação no seu CMD):
# pip install streamlit pandas pydeck

import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

# --- Configuração da Aplicação ---
st.set_page_config(page_title="GPS Navigator (PyDeck Demo)", layout="centered")
st.title("🗺️ Navegação GPS Simples")
st.caption("Insira os detalhes de Origem e Destino para visualizar a rota.")

# --- Dados de Exemplo (SUAS COORDENADAS) ---

# Defina as coordenadas DE PADRÃO (Exemplo: São Paulo Capital e Interior)
DEFAULT_ORIGEM_LAT = -23.5505  # Exemplo: São Paulo - Capital
DEFAULT_ORIGEM_LON = -46.6333

DEFAULT_DESTINO_LAT = -23.0121  # Exemplo: Bom Jesus dos Perdões (sua cidade)
DEFAULT_DESTINO_LON = -46.4011

# --- Interface para Configuração das Coordenadas ---

st.sidebar.header("📍 Configurações de Rota")

# Entrada de dados (mantidas na barra lateral para limpeza)
origem_nome = st.sidebar.text_input("Nome da Origem", "Minha Casa (SP Capital)")
destino_nome = st.sidebar.text_input("Nome do Destino", "Target (Bom Jesus dos Perdões)")

# Usando colunas para melhor organização dos inputs de coordenadas no corpo principal
st.subheader("Inserir Coordenadas (Latitude e Longitude)")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Origem")
    # Agora as coordenadas são lidas dos inputs e usadas nos DataFrames
    origem_lat = st.number_input("Latitude (Origem)", value=DEFAULT_ORIGEM_LAT, format="%.4f")
    origem_lon = st.number_input("Longitude (Origem)", value=DEFAULT_ORIGEM_LON, format="%.4f")

with col2:
    st.markdown("#### Destino")
    destino_lat = st.number_input("Latitude (Destino)", value=DEFAULT_DESTINO_LAT, format="%.4f")
    destino_lon = st.number_input("Longitude (Destino)", value=DEFAULT_DESTINO_LON, format="%.4f")


# Criação dos DataFrames com base nas entradas do usuário
origem_data = pd.DataFrame([
    {"name": origem_nome, "lat": origem_lat, "lon": origem_lon, "color": [0, 255, 0, 255]} # Verde
])

destino_data = pd.DataFrame([
    {"name": destino_nome, "lat": destino_lat, "lon": destino_lon, "color": [255, 0, 0, 255]} # Vermelho
])

# Rota
route_data = pd.DataFrame([{
    "lon": origem_lon,
    "lat": origem_lat,
    "lon2": destino_lon,
    "lat2": destino_lat,
}])


try:
    # --- 3. Camadas do Pydeck ---

    # Camada 1: Ponto de Origem (Verde)
    origin_layer = pdk.Layer(
        "ScatterplotLayer",
        data=origem_data,
        get_position=["lon", "lat"],
        get_color=[0, 255, 0, 200], # Verde
        get_radius=1000, # Raio em metros
        pickable=True,
    )

    # Camada 2: Ponto de Destino (Vermelho)
    destination_layer = pdk.Layer(
        "ScatterplotLayer",
        data=destino_data,
        get_position=["lon", "lat"],
        get_color=[255, 0, 0, 200], # Vermelho
        get_radius=1000,
        pickable=True,
    )

    # Camada 3: Rota (Linha de Arco entre Origem e Destino)
    route_layer = pdk.Layer(
        "ArcLayer",
        data=route_data,
        get_source_position=["lon", "lat"],
        get_target_position=["lon2", "lat2"],
        get_source_color=[0, 255, 0, 160], # Origem Verde
        get_target_color=[255, 0, 0, 160], # Destino Vermelho
        auto_highlight=True,
        width_min_pixels=5,
    )

    # Configuração da Visualização Inicial (Centralizado entre os pontos)
    view_state = pdk.ViewState(
        latitude=(origem_lat + destino_lat) / 2, # Latitude média
        longitude=(origem_lon + destino_lon) / 2, # Longitude média
        zoom=9, # Zoom inicial para ver os dois pontos
        pitch=45,
    )

    # Exibe o mapa no Streamlit
    st.pydeck_chart(
        pdk.Deck(
            # Corrigido: Usando o estilo "dark" que é padrão e confiável para carregamento.
            map_style="dark", 
            initial_view_state=view_state,
            layers=[origin_layer, destination_layer, route_layer],
        )
    )

    # --- Tabela de Dados (Debug/Informação) ---
    st.markdown("---")
    st.subheader("Detalhes dos Pontos")
    
    # Combine e exiba os dados para referência
    combined_data = pd.concat([
        origem_data.rename(columns={'name': 'Local'}), 
        destino_data.rename(columns={'name': 'Local'})
    ])
    combined_data['Tipo'] = ['Origem', 'Destino']
    st.dataframe(combined_data[['Tipo', 'Local', 'lat', 'lon']].reset_index(drop=True))

except URLError as e:
    st.error(
        f"""
        **Este aplicativo requer acesso à internet.**
        Erro de Conexão: {e.reason}
        """
    )