# Arquivo: streamlit_chat_app.py
#
# Este script cria uma aplicação web de chat interativo usando Streamlit
# e a API da NVIDIA (compatível com OpenAI), agora com o tema "Matrix Green".
#
# Pré-requisitos (Instalação no seu CMD):
# pip install streamlit openai

import streamlit as st
from openai import OpenAI

# --- Configuração da API (Usando as chaves e modelos comprovados) ---
NVIDIA_API_KEY = ""
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
LLM_MODEL = "meta/llama3-8b-instruct"

# --- 1. CONFIGURAÇÃO VISUAL (TEMA MATRIX GREEN + LOGO) ---

# URL de um logotipo simples da NVIDIA para uso em apps (verde)
NVIDIA_LOGO_URL = "https://build.nvidia.com/_next/image?url=%2Fnvidia-logo.png&w=300&q=75"

# URL de placeholder para o avatar da IA (Bordas arredondadas/circulares)
# ATENÇÃO: Substitua este link pelo URL COMPLETO e ACESSÍVEL da sua imagem.
# Exemplo: AI_AVATAR_URL = "https://exemplo.com/f76d2255d0608ef89ad6c4742ad7fc8e~tplv-tiktokx-cropcenter_1080_1080.jpeg"
AI_AVATAR_URL = "https://placehold.co/40x40/00FF41/000000?text=AI" 

# Custom CSS para o tema Matrix Green
st.markdown("""
    <style>
        /* Fundo principal escuro */
        .stApp {
            background-color: #000000;
            color: #00FF41; /* Texto principal em verde Matrix */
        }
        /* Cor do texto geral */
        * {
            color: #00FF41 !important;
        }
        /* Fundo da barra lateral */
        .stSidebar {
            background-color: #000000;
        }
        /* Chat bubble do assistente */
        .stChatMessage [data-testid="stChatMessageContent"] {
            background-color: #0A0A0A !important; /* Quase preto */
            border-left: 5px solid #00FF41;
            color: #00FF41 !important;
        }
        /* Chat bubble do usuário */
        .st-emotion-cache-1c5t18c.e1ywh95f0 { /* Seletor do input do chat */
            background-color: #0A0A0A !important;
            border-top: 1px solid #00FF41;
        }
        .st-emotion-cache-1629p8f.e1ywh95f0 {
            color: #00FF41 !important;
        }
        /* Botão de envio e input field */
        [data-testid="stForm"] > button {
             background-color: #00FF41 !important;
             color: #000000 !important; /* Texto do botão em preto */
             font-weight: bold;
        }
        [data-testid="stTextInput"] > div > div > input {
            background-color: #0A0A0A !important;
            border: 1px solid #00FF41;
            color: #00FF41 !important;
        }
    </style>
    """, unsafe_allow_html=True)


st.set_page_config(page_title="NVIDIA AI Chat (Matrix)", layout="centered")

# Adicionar o logo da NVIDIA na barra lateral
st.sidebar.image(NVIDIA_LOGO_URL, width=150)
st.sidebar.markdown("<h2 style='color:#00FF41;'>NVIDIA AI Chat</h2>", unsafe_allow_html=True)
st.sidebar.write(f"Modelo: **`{LLM_MODEL}`**")
st.sidebar.markdown("---")

# NOVO TÍTULO: Usando st.markdown para inserir a imagem arredondada (como uma bola)
st.markdown(
    f"""
    <div style='display: flex; align-items: center;'>
        <img src="{AI_AVATAR_URL}" 
             alt="AI Avatar" 
             style="border-radius: 50%; width: 40px; height: 40px; margin-right: 10px; border: 2px solid #00FF41;">
        <h1 style='color:#00FF41; margin: 0;'>Chat com IA (Tema Matrix)</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.caption("A cor do tema foi alterada para verde Matrix e o robô foi substituído por um avatar circular.")


# --- Configuração do Cliente API ---

# Inicializa o cliente da OpenAI para o endpoint da NVIDIA
@st.cache_resource
def get_openai_client():
    """Inicializa e armazena o cliente OpenAI (NVIDIA) em cache."""
    try:
        client = OpenAI(
            base_url=NVIDIA_BASE_URL,
            api_key=NVIDIA_API_KEY
        )
        return client
    except Exception as e:
        st.error(f"Erro ao inicializar o cliente da API: {e}")
        return None

client = get_openai_client()

# Inicializa o histórico de mensagens no st.session_state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Olá! Este chat agora tem o visual verde Matrix. Pergunte-me qualquer coisa!"}
    ]

# --- Exibir o Histórico de Mensagens ---
for msg in st.session_state.messages:
    # Usa o componente de chat nativo do Streamlit
    st.chat_message(msg["role"]).write(msg["content"])

# --- Lógica de Entrada e Resposta ---

if prompt := st.chat_input("Digite sua pergunta aqui..."):
    if not client:
        st.error("O cliente da API não foi inicializado corretamente.")
        st.stop()

    # 1. Adiciona a mensagem do usuário ao histórico e exibe
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 2. Faz a chamada à API com o histórico completo
    try:
        with st.chat_message("assistant"):
            with st.spinner("Aguardando resposta da NVIDIA..."):

                completion = client.chat.completions.create(
                    model=LLM_MODEL,
                    messages=st.session_state.messages, # Envia todo o histórico
                    stream=False
                )

                # 3. Processa e exibe a resposta do assistente
                assistant_response = completion.choices[0].message.content
                st.write(assistant_response)

        # 4. Adiciona a resposta do assistente ao histórico da sessão
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    except Exception as e:
        error_message = f"Erro ao chamar a API: {e}"
        if "404" in str(e):
            error_message = f"Erro 404: Modelo '{LLM_MODEL}' não encontrado. Verifique o nome exato no painel da NVIDIA."
        elif "401" in str(e):
            error_message = "Erro 401: Chave de API inválida ou expirada."

        st.error(error_message)
        # Remove a última mensagem do usuário para não poluir o histórico com a tentativa falha
        st.session_state.messages.pop()