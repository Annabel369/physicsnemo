# Arquivo: fractal_generator_app.py
#
# Aplicação Streamlit que gera um Fractal (Conjunto de Júlia)
# de forma interativa com base nas configurações do usuário.
#
# Pré-requisitos (Instalação no seu CMD):
# pip install streamlit numpy

import streamlit as st
import numpy as np
from typing import Any

# --- Configuração da Aplicação ---
st.set_page_config(page_title="Gerador de Fractais Interativo", layout="centered")

# --- Cabeçalho e Descrição ---
st.title("🎨 Gerador de Desenho Fractal")
st.caption("Ajuste os parâmetros na barra lateral para mudar o padrão do Fractal de Júlia.")

# --- Barra Lateral (Controles do Usuário) ---
st.sidebar.header("⚙️ Controles do Desenho")

# Interactive Streamlit elements, like these sliders, return their value.
iterations = st.sidebar.slider("Nível de Detalhe (Iterações)", 2, 50, 20, 1)
separation = st.sidebar.slider("Fator de Separação", 0.7, 2.0, 0.7885)

# Não precisamos da lógica de barra de progresso e frame_text para esta demonstração simples.
# Os placeholders (frame_text, progress_bar) foram removidos para simplificar o código.

# --- Renderização do Fractal ---

# Elemento placeholder para a imagem do fractal
image_placeholder = st.empty()

# Dimensões da tela de cálculo
m, n, s = 960, 640, 400
x = np.linspace(-m / s, m / s, num=m).reshape((1, m))
y = np.linspace(-n / s, n / s, num=n).reshape((n, 1))

# O Streamlit roda o script do topo para baixo sempre que um slider muda.
# Portanto, a lógica de loop de animação (for frame_num in...) do seu exemplo original
# não é necessária. Em vez disso, calculamos o fractal com os valores atuais dos sliders.

# Para manter o desenho dinâmico, vamos usar um valor 'a' (ângulo) fixo, 
# mas que muda suavemente ao longo do tempo (usando o tempo de execução).
# Usaremos um índice simples de tempo para fazer uma animação sutil.
if 'a_index' not in st.session_state:
    st.session_state.a_index = 0
st.session_state.a_index += 0.05
if st.session_state.a_index > 4 * np.pi:
    st.session_state.a_index = 0.05

a = st.session_state.a_index

# --- CÁLCULO DO FRACTAL DE JÚLIA ---
c = separation * np.exp(1j * a)
z = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
c_matrix = np.full((n, m), c)

# m_matrix: Qualquer tipo de dados que possa ser usado como máscara booleana (True/False)
m_matrix: Any = np.full((n, m), True, dtype=bool) 
n_matrix = np.zeros((n, m))

for i in range(iterations):
    # A atualização da matriz 'z' é feita apenas onde m_matrix é True
    z[m_matrix] = z[m_matrix] * z[m_matrix] + c_matrix[m_matrix]
    
    # Atualiza a máscara: onde o módulo de z for maior que 2, o ponto "escapou"
    newly_escaped = np.abs(z) > 2
    
    # Marca os pontos que escaparam na iteração atual
    escaped_in_this_step = m_matrix & newly_escaped
    
    # Marca o número da iteração para os pontos que escaparam neste passo
    n_matrix[escaped_in_this_step] = i 
    
    # Remove os pontos que escaparam da máscara para não serem processados novamente
    m_matrix[newly_escaped] = False

# Tratamento de cores: Normaliza a matriz de iterações para o intervalo [0.0, 1.0]
# Adiciona 1 para evitar divisão por zero (que ocorre se todos os pontos convergirem)
color_data = 1.0 - (n_matrix / (n_matrix.max() + 1)) 

# O image_placeholder é atualizado chamando image()
image_placeholder.image(color_data, use_container_width=True, channels="GRAY")
# --- FIM DO CÁLCULO E RENDERIZAÇÃO ---

# O botão Rerun força o script a rodar novamente.
if st.button("Forçar Nova Renderização"):
    st.session_state.a_index = 0.05 # Reseta o ângulo se necessário

st.info(f"O fractal está sendo renderizado com {iterations} iterações e fator de separação de {separation}.")

# Para manter a animação sutil rodando (o 'a' index), precisamos de uma forma de re-rodar o script.
# Como fizemos um pequeno avanço em st.session_state.a_index, vamos re-rodar
# o Streamlit automaticamente a cada 100ms para criar a ilusão de movimento.
st.rerun()