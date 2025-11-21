# 🔍 Sistema de Ingestão e Busca Semântica com LangChain e PostgreSQL

Sistema completo de processamento de PDFs com busca semântica utilizando LangChain, PostgreSQL + pgVector e modelos de IA (OpenAI ou Google Gemini).

## 📋 Funcionalidades

- **Ingestão de PDF**: Processa documentos PDF, divide em chunks e armazena embeddings no banco vetorial
- **Busca Semântica**: Realiza buscas por similaridade usando vetores
- **Chat Interativo**: Interface CLI para fazer perguntas sobre o conteúdo do PDF
- **Suporte Multi-Provider**: Compatível com OpenAI e Google Gemini

## 🛠️ Tecnologias

- **Python 3.8+**
- **LangChain**: Framework para aplicações com LLMs
- **PostgreSQL + pgVector**: Banco de dados vetorial
- **Docker & Docker Compose**: Containerização do banco de dados
- **OpenAI API** ou **Google Gemini API**: Modelos de embeddings e LLM

## 📦 Estrutura do Projeto

```
├── docker-compose.yml      # Configuração do PostgreSQL com pgVector
├── requirements.txt        # Dependências Python
├── .env.example           # Template das variáveis de ambiente
├── src/
│   ├── ingest.py         # Script de ingestão do PDF
│   ├── search.py         # Script de busca semântica
│   └── chat.py           # Interface CLI interativa
├── document.pdf          # PDF para ingestão (adicione seu arquivo)
└── README.md             # Este arquivo
```

## 🚀 Instalação e Configuração

### 1. Pré-requisitos

- Python 3.8 ou superior
- Docker e Docker Compose instalados
- Conta OpenAI ou Google Cloud (para APIs)

### 2. Criar e Ativar Ambiente Virtual

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar no Linux/Mac
source venv/bin/activate

# Ativar no Windows
venv\Scripts\activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e configure suas credenciais:

**Para OpenAI:**
```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-api-key-here
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
```

**Para Google Gemini:**
```env
AI_PROVIDER=gemini
GOOGLE_API_KEY=your-google-api-key-here
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
```

### 5. Subir o Banco de Dados

```bash
docker compose up -d
```

Aguarde o banco inicializar (cerca de 10 segundos). Verifique o status:

```bash
docker compose ps
```

## 📖 Como Usar

### Passo 1: Adicionar o PDF

Coloque seu arquivo PDF na raiz do projeto com o nome `document.pdf`, ou edite o caminho no script `src/ingest.py`.

### Passo 2: Executar Ingestão

Execute o script de ingestão para processar o PDF e armazenar no banco:

```bash
python src/ingest.py
```

**Saída esperada:**
```
🔄 Iniciando processo de ingestão...
📄 Carregando PDF: document.pdf
✅ PDF carregado: 10 página(s)
✂️  Dividindo documento em chunks...
✅ Documento dividido em 87 chunks
🔧 Configurando modelo de embeddings...
✅ Usando provider: openai
💾 Armazenando 87 chunks no banco de dados...
⏳ Este processo pode levar alguns minutos...
✅ Ingestão concluída com sucesso!
📊 Total de chunks armazenados: 87
📦 Coleção: pdf_documents
```

### Passo 3: Rodar o Chat Interativo

Inicie o chat para fazer perguntas:

```bash
python src/chat.py
```

**Exemplo de interação:**

```
============================================================
🤖 Sistema de Busca Semântica em PDF
============================================================
📡 Provider: OPENAI
💡 Digite 'sair' ou 'exit' para encerrar
============================================================

Faça sua pergunta:

PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
🔍 Buscando informações...
RESPOSTA: O faturamento foi de 10 milhões de reais.

------------------------------------------------------------

Faça sua pergunta:

PERGUNTA: Quantos clientes temos em 2024?
🔍 Buscando informações...
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.

------------------------------------------------------------

PERGUNTA: sair
👋 Encerrando o chat. Até logo!
```

## 🔧 Configurações Técnicas

### Modelos Utilizados

**OpenAI:**
- Embeddings: `text-embedding-3-small`
- LLM: `gpt-4o-mini` (ajustável no código)

**Google Gemini:**
- Embeddings: `models/embedding-001`
- LLM: `gemini-2.0-flash-exp` (ajustável no código)

### Parâmetros de Chunking

- **Chunk Size**: 1000 caracteres
- **Overlap**: 150 caracteres
- **Resultados por busca (k)**: 10

### Banco de Dados

- **Host**: localhost
- **Porta**: 5432
- **Usuário**: postgres
- **Senha**: postgres
- **Database**: vectordb

## 🐛 Troubleshooting

### Erro: "OPENAI_API_KEY não encontrada"
Verifique se o arquivo `.env` existe e contém a chave de API válida.

### Erro: "Arquivo não encontrado: document.pdf"
Certifique-se de que o arquivo PDF está na raiz do projeto ou ajuste o caminho em `src/ingest.py`.

### Erro de conexão com o banco
Verifique se o Docker está rodando e se o container PostgreSQL está ativo:
```bash
docker compose ps
docker compose logs postgres
```

### Reiniciar o banco de dados
```bash
docker compose down
docker compose up -d
```

## 🧹 Limpeza

Para parar e remover o banco de dados:

```bash
# Parar os containers
docker compose down

# Remover volumes (apaga os dados)
docker compose down -v
```

## 📝 Notas Importantes

- O sistema responde apenas com base no conteúdo do PDF processado
- Perguntas fora do contexto retornarão a mensagem padrão de "informações não disponíveis"
- O processo de ingestão pode demorar dependendo do tamanho do PDF

## 🤝 Suporte

Para problemas ou dúvidas:
1. Verifique se todas as dependências foram instaladas
2. Confirme que as variáveis de ambiente estão configuradas
3. Verifique os logs do Docker: `docker compose logs`

## 📄 Licença

Este projeto é fornecido como exemplo educacional.