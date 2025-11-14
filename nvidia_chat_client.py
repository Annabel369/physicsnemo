# Arquivo: nvidia_chat_client.py
#
# Terminal de Chat Interativo: Permite que o usuário converse com o modelo
# 'meta/llama3-8b-instruct' da NVIDIA, mantendo o histórico da conversa.
#
# Pré-requisito: Você deve ter a biblioteca 'openai' instalada:
# pip install openai
#
# Para executar: python nvidia_chat_client.py

from openai import OpenAI
import sys

# --- Configuração da API ---
NVIDIA_API_KEY = ""
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
LLM_MODEL = "meta/llama3-8b-instruct" # Modelo Conversacional comprovadamente funcional

# Inicializa o histórico de mensagens com a saudação
messages = [
    {"role": "assistant", "content": "Olá! Eu sou um assistente de IA. Qual é a sua primeira pergunta sobre tecnologia?"}
]

print("-" * 50)
print(f"Bem-vindo ao Chat Terminal (Modelo: {LLM_MODEL})")
print("Digite 'sair' ou 'exit' para encerrar a conversa.")
print("-" * 50)

# Imprime a primeira mensagem do assistente
print(f"Assistente: {messages[0]['content']}")


try:
    # 1. Configura o cliente da OpenAI para apontar para o endpoint da NVIDIA
    client = OpenAI(
      base_url = NVIDIA_BASE_URL,
      api_key = NVIDIA_API_KEY
    )

    while True:
        # 2. Obtém a entrada do usuário
        user_input = input("\nVocê: ")

        # Verifica condição de saída
        if user_input.lower() in ["sair", "exit"]:
            print("\nEncerrando a sessão. Até mais!")
            break

        # Adiciona a mensagem do usuário ao histórico
        messages.append({"role": "user", "content": user_input})

        # 3. Faz a chamada à API com o histórico completo
        print(f"Enviando solicitação à API da NVIDIA...")
        completion = client.chat.completions.create(
          model=LLM_MODEL,
          messages=messages, # Envia todo o histórico
          stream=False
        )

        # 4. Processa e imprime a resposta do assistente
        assistant_response = completion.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_response})
        
        print(f"Assistente: {assistant_response}")

except Exception as e:
    # Tratamento de erro detalhado
    if "401" in str(e):
        print(f"\n[ERRO] Ocorreu um erro 401 (Não Autorizado). Verifique a validade da sua chave de API.")
    elif "404" in str(e):
        print(f"\n[ERRO] Ocorreu um erro 404 (Modelo Não Encontrado).")
        print(f"Verifique se o modelo '{LLM_MODEL}' está ativado para sua chave no painel da NVIDIA.")
    else:
        print(f"\n[ERRO] Ocorreu um erro inesperado: {e}")
        print("Verifique sua conectividade e a validade da chave/modelo.")