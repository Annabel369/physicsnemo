import torch
from physicsnemo.models.burgers import BurgersModel

# Inicializa o modelo de Burgers com parâmetros padrão
modelo = BurgersModel()

# Cria dados de entrada fictícios (exemplo: velocidade inicial)
entrada = torch.randn(1, 2)  # 1 amostra, 2 variáveis (ex: tempo e posição)

# Executa a simulação
saida = modelo.forward(entrada)

# Exibe o resultado
print("🌀 Resultado da simulação Burgers:")
print(saida)