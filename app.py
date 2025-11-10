import streamlit as st
import torch
import matplotlib.pyplot as plt

# Tenta importar o modelo Darcy
try:
    from physicsnemo.models.darcy import DarcyModel
except ImportError:
    st.error("❌ Não foi possível importar DarcyModel. Verifique se está disponível em physicsnemo.models.darcy.")
    st.stop()

st.title("🧪 Simulação Darcy com PhysicsNeMo")

# Parâmetros de entrada
st.sidebar.header("🔧 Parâmetros de entrada")
pressao = st.sidebar.slider("Pressão", min_value=0.0, max_value=100.0, value=50.0, step=1.0)
porosidade = st.sidebar.slider("Porosidade", min_value=0.0, max_value=1.0, value=0.5, step=0.01)

# Botão para executar
if st.button("Executar Simulação"):
    modelo = DarcyModel()

    entrada = torch.tensor([[pressao, porosidade]], dtype=torch.float32)

    try:
        saida = modelo.forward(entrada)
        resultado = saida.detach().numpy()

        st.success("✅ Simulação concluída!")
        st.write("Resultado:", resultado)

        fig, ax = plt.subplots()
        ax.plot(resultado[0])
        ax.set_title("Resultado da Simulação Darcy")
        ax.set_xlabel("Índice")
        ax.set_ylabel("Valor")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Erro ao executar o modelo: {e}")