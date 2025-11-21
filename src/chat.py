import os
from search import search_prompt

def main():
    print("=" * 60)
    print("🤖 Sistema de Busca Semântica em PDF")
    print("Aluno: Luiz Fernando Calazans Pereira Filho")
    print("=" * 60)
    provider = os.getenv("AI_PROVIDER", "openai")
    print(f"📡 Provider: {provider.upper()}")
    print("💡 Digite 'sair' ou 'exit' para encerrar")
    print("=" * 60)
    print("Inicializando sistema de busca...")
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        print("Possíveis erros:")
        print("- PostgreSQL db não está up")
        print("- As variáveis de ambiente estão configuradas incorretamente no .env")
        print("- A ingestão do PDF não foi executada com sucesso")
        return
    
    print("Sistema inicializado com sucesso!")
    print("\n" + "=" * 50)
    
    while True:
        try:
            
            question = input("\nFaça sua pergunta: ").strip()
                        
            if question.lower() in ['sair', 'quit', 'exit', 'q']:
                print("Encerrando o chat...")
                break
               
            if not question:
                print("Por favor, digite uma pergunta válida.")
                continue
            
            print(f"\nPERGUNTA: {question}")
            print("Buscando informações relevantes...")
            
            resposta = chain.invoke(question)
            
            print("=" * 50)
            print(f"RESPOSTA: {resposta}")
            print("=" * 50)
            
        except KeyboardInterrupt:
            print("\nChat interrompido pelo usuário.")
            break
        except Exception as e:
            print(f"Erro ao processar a pergunta: {e}")
            print(f"Erro ao processar a pergunta: {e.__traceback__}")
            print("Tente novamente com uma pergunta diferente.")
            raise e

if __name__ == "__main__":
    main()