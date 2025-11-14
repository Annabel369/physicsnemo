/**
 * Arquivo: nvidia_chat_client.js
 *
 * Demonstra como se conectar à API da NVIDIA (compatível com OpenAI) usando Node.js.
 *
 * Configuração:
 * 1. npm install openai
 * 2. Salve este arquivo.
 * 3. Execute: node nvidia_chat_client.js
 */

// Usamos 'require' para maior compatibilidade com diferentes ambientes Node.js.
const OpenAI = require('openai');

// --- Configuração da API ---
// Sua chave de API da NVIDIA.
const NVIDIA_API_KEY = "";
const NVIDIA_BASE_URL = 'https://integrate.api.nvidia.com/v1';

const client = new OpenAI({
  apiKey: NVIDIA_API_KEY,
  baseURL: NVIDIA_BASE_URL,
});

// A conversa traduzida para o português.
const messages = [
    {"role":"user","content":"Esqueci como encerrar um processo no Linux, você pode me ajudar?"},
    {"role":"assistant","content":"Claro! Para encerrar um processo no Linux, você pode usar o comando kill, seguido pelo Process ID (PID) do processo que deseja encerrar."},
    {"role": "user", "content": "Ótimo, por favor, forneça um comando específico para encontrar o PID."}
];

async function runSafetyGuardTest() {
    // Modelo de Segurança: Retorna JSON de classificação.
    const LLM_MODEL = "nvidia/llama-3.1-nemotron-safety-guard-8b-v3";
    console.log(`\n--- Teste 1: Modelo Safety Guard (${LLM_MODEL}) ---`);
    console.log("Aguardando JSON de Classificação de Segurança...");
    
    try {
        const completion = await client.chat.completions.create({
            model: LLM_MODEL,
            messages: messages,
            stream: false,
        });

        console.log("\n[Resposta do Modelo Safety Guard - JSON de Classificação]");
        console.log("Role:", completion.choices[0]?.message?.role);
        // O modelo Safety Guard retorna um JSON com a classificação de segurança.
        console.log("Content:", completion.choices[0]?.message?.content); 
        
    } catch (error) {
        console.error(`\nErro ao chamar Safety Guard API: ${error.message}`);
    }
}

async function runConversationalTest() {
    // NOVA TENTATIVA: Usando o prefixo 'meta/' para o modelo Llama 3 8B Instruct, que é comum na API da NVIDIA.
    const LLM_MODEL = "meta/llama3-8b-instruct"; 
    console.log(`\n--- Teste 2: Modelo Conversacional (${LLM_MODEL}) ---`);
    console.log("Aguardando Resposta Conversacional...");

    try {
        const completion = await client.chat.completions.create({
            model: LLM_MODEL,
            messages: messages,
            stream: false,
        });

        console.log("\n[Resposta do Modelo Conversacional]");
        console.log("Role:", completion.choices[0]?.message?.role);
        console.log("Content:", completion.choices[0]?.message?.content);
        
    } catch (error) {
        console.error(`\nErro ao chamar Conversational API: ${error.message}`);
        console.log("Atenção: A NVIDIA usa nomes de modelos muito específicos. Se o erro 404 persistir, a verificação no seu painel da NVIDIA é obrigatória.");
    }
}

async function main() {
    await runSafetyGuardTest();
    await runConversationalTest();
}

main();