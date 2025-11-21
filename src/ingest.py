import os
from pathlib import Path
from dotenv import load_dotenv
import httpx
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()

def get_embeddings():
    provider = os.getenv("AI_PROVIDER", "openai").lower()
    http_client = httpx.Client(verify=False)
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY não está definido.")
        return OpenAIEmbeddings(
            openai_api_key=api_key,
            model="text-embedding-3-small",
            http_client=http_client
        )
        
    elif provider == 'gemini':
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY não está definido.")
        return GoogleGenerativeAIEmbeddings(
            google_api_key=api_key,
            model="models/embedding-001"
        )
    else:
        raise ValueError(f"Provider '{provider}' não suportado. Use 'openai' ou 'gemini'")

def ingest_pdf():
    print("🔄 Iniciando processo de ingestão...")

    documents = import_pdf_data()

    chunks = generate_chunks(documents)
    
    embeddings = setup_embeddings()

    database_url = retrieve_database_url()
    collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME")
    
    print(f"💾 Armazenando {len(chunks)} chunks no banco de dados...")
    print("⏳ Este processo pode levar alguns minutos...")

    vector_store = PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        connection=database_url,
        use_jsonb=True
    )
    print(f"✅ Ingestão concluída com sucesso!")
    print(f"📊 Total de chunks armazenados: {len(chunks)}")
    print(f"📦 Coleção: {collection_name}")

    return vector_store

def import_pdf_data():
    current_dir = Path(__file__).parent.parent
    pdf_path = current_dir / "document.pdf"
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF não encontrado: {pdf_path}")

    print(f"📄 Carregando PDF: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"✅ PDF carregado: {len(documents)} página(s)")
    return documents

def setup_embeddings():
    print("🔧 Configurando modelo de embeddings...")
    embeddings = get_embeddings()
    provider = os.getenv("AI_PROVIDER", "openai")
    print(f"✅ Usando provider: {provider}")
    return embeddings

def generate_chunks(documents):
    print("✂️  Dividindo documento em chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Documento dividido em {len(chunks)} chunks")
    return chunks

def retrieve_database_url():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL não encontrada no arquivo .env")
    return database_url


if __name__ == "__main__":
    try:
        ingest_pdf()
    except Exception as e:
        print(f"❌ Erro durante a ingestão: {str(e)}")
        raise