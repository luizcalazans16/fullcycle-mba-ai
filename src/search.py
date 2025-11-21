import os
from dotenv import load_dotenv
import httpx
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_postgres import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

load_dotenv()

def format_docs(docs):
    return "\n\n".join([f"Documento {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])


def get_embeddings():
    provider = os.getenv("AI_PROVIDER", "openai").lower()
    http_client = httpx.Client(verify=False)

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY não encontrada no arquivo .env")
        return OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=api_key,
            http_client=http_client
        )
    elif provider == "gemini":
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY não encontrada no arquivo .env")
        return GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key
        )
    else:
        raise ValueError(f"Provider '{provider}' não suportado")


def get_llm():
    provider = os.getenv("AI_PROVIDER", "openai").lower()
    http_client = httpx.Client(verify=False)

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY não está definido.")
        return ChatOpenAI(
            model="gpt-4o-mini",  # Usando gpt-4o-mini pois gpt-5-nano não existe ainda
            temperature=0,
            openai_api_key=api_key,
            http_client=http_client
        )
    elif provider == "gemini":
        api_key = os.getenv("GOOGLE_API_KEY")
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",  # Usando modelo disponível
            temperature=0,
            google_api_key=api_key
        )
    else:
        raise ValueError(f"Provider '{provider}' não suportado")


def get_vectorstore():
    """Conecta ao vectorstore existente"""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL não encontrada no arquivo .env")

    embeddings = get_embeddings()

    vectorstore = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=database_url,
        use_jsonb=True
    )

    return vectorstore

def format_docs(docs):
    return "\n\n".join([f"Documento {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])

def search_prompt():
    try:
        vector_store = get_vectorstore()
        retriever = vector_store.as_retriever(search_kwargs={"k": 10})
        
        llm = get_llm()
        
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        
        rag_chain = (
            {"contexto": retriever | format_docs, "pergunta": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        return rag_chain
        
    except Exception as e:
        print(f"Erro ao configurar a busca: {e.__traceback__}")
        raise e