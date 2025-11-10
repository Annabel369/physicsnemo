from physicsnemo.models import Module

def responder_pergunta(pergunta):
    pergunta = pergunta.lower()
    if "modelo" in pergunta:
        return "Você pode usar módulos como Burgers, Navier-Stokes ou Darcy para simular fenômenos físicos."
    elif "cuda" in pergunta:
        return "Sim, o PhysicsNeMo suporta execução em CUDA para acelerar simulações com GPU."
    elif "parâmetro" in pergunta:
        return "Você pode acessar os parâmetros de um módulo com .parameters() ou .named_parameters()."
    else:
        return "Ainda estou aprendendo sobre isso. Tente perguntar sobre modelos, dispositivos ou parâmetros."

# Inicializa um módulo genérico
modulo = Module()

# Loop de interação com comando de saída
print("🤖 PhysicsNeMo Chat iniciado! Digite 'sair' para encerrar.")
while True:
    try:
        pergunta = input("Você: ")
        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("👋 Encerrando o chat. Até mais!")
            break
        resposta = responder_pergunta(pergunta)
        print("PhysicsNeMo:", resposta)
    except KeyboardInterrupt:
        print("\n👋 Encerrando o chat por interrupção. Até mais!")
        break