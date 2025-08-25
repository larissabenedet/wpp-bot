"""
Script para explorar e gerenciar o banco de dados.
Use este script para ver dados, adicionar usuários de teste, etc.
"""
from app.database.database import SessionLocal
from app.database.models import User, Question, UserResponse, TechArea, Language
from app.database.crud import *
from sqlalchemy import text

def show_all_tables():
    """Mostra todas as tabelas e seus dados"""
    db = SessionLocal()
    
    try:
        print("=" * 50)
        print("📊 EXPLORANDO O BANCO DE DADOS")
        print("=" * 50)
        
        # Contar registros em cada tabela
        users_count = db.query(User).count()
        questions_count = db.query(Question).count()
        responses_count = db.query(UserResponse).count()
        
        print(f"\n📈 ESTATÍSTICAS:")
        print(f"👥 Usuários: {users_count}")
        print(f"❓ Perguntas: {questions_count}")
        print(f"💬 Respostas: {responses_count}")
        
        # Mostrar usuários
        print(f"\n👥 USUÁRIOS REGISTRADOS:")
        users = db.query(User).all()
        if users:
            for user in users:
                status = "🟢 Ativo" if user.is_active else "🔴 Inativo"
                print(f"  • {user.whatsapp_number} | {user.name} | {user.tech_area.value} | {status}")
        else:
            print("  Nenhum usuário registrado ainda")
        
        # Mostrar perguntas por categoria
        print(f"\n❓ PERGUNTAS POR CATEGORIA:")
        for tech_area in TechArea:
            count = db.query(Question).filter(Question.tech_area == tech_area).count()
            print(f"  • {tech_area.value}: {count} perguntas")
        
        # Mostrar algumas perguntas
        print(f"\n📝 EXEMPLOS DE PERGUNTAS:")
        sample_questions = db.query(Question).limit(3).all()
        for q in sample_questions:
            print(f"  • [{q.tech_area.value}] {q.question_text_pt[:60]}...")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        db.close()

def add_test_user():
    """Adiciona um usuário de teste"""
    db = SessionLocal()
    
    try:
        # Verificar se já existe
        existing = get_user_by_whatsapp(db, "+5511999999999")
        if existing:
            print("👤 Usuário de teste já existe!")
            return
        
        # Criar usuário de teste
        test_user = create_user(
            db=db,
            whatsapp_number="+5511999999999",
            name="Usuário Teste",
            preferred_language=Language.PORTUGUESE,
            tech_area=TechArea.JAVASCRIPT
        )
        
        print(f"✅ Usuário de teste criado: {test_user.whatsapp_number}")
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário: {e}")
    finally:
        db.close()

def show_questions_by_area(tech_area: str):
    """Mostra perguntas de uma área específica"""
    db = SessionLocal()
    
    try:
        area_enum = TechArea(tech_area.lower())
        questions = get_questions_by_area(db, area_enum)
        
        print(f"\n❓ PERGUNTAS DE {tech_area.upper()}:")
        for i, q in enumerate(questions, 1):
            print(f"\n{i}. [{q.difficulty}] {q.question_text_pt}")
            if q.expected_concepts:
                print(f"   Conceitos: {q.expected_concepts}")
        
    except ValueError:
        print(f"❌ Área inválida. Use: javascript, python, ruby, dsa")
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        db.close()

def run_custom_query(query: str):
    """Executa uma query SQL customizada"""
    db = SessionLocal()
    
    try:
        result = db.execute(text(query))
        rows = result.fetchall()
        
        print(f"\n🔍 RESULTADO DA QUERY:")
        print(f"Query: {query}")
        print("-" * 40)
        
        for row in rows:
            print(row)
            
    except Exception as e:
        print(f"❌ Erro na query: {e}")
    finally:
        db.close()

def main_menu():
    """Menu interativo para explorar o banco"""
    while True:
        print("\n" + "=" * 40)
        print("🗄️  EXPLORADOR DO BANCO DE DADOS")
        print("=" * 40)
        print("1. 📊 Ver estatísticas gerais")
        print("2. 👤 Adicionar usuário de teste")
        print("3. ❓ Ver perguntas por área")
        print("4. 🔍 Executar query customizada")
        print("5. 🚪 Sair")
        
        choice = input("\nEscolha uma opção (1-5): ").strip()
        
        if choice == "1":
            show_all_tables()
        elif choice == "2":
            add_test_user()
        elif choice == "3":
            area = input("Digite a área (javascript/python/ruby/dsa): ").strip()
            show_questions_by_area(area)
        elif choice == "4":
            query = input("Digite a query SQL: ").strip()
            run_custom_query(query)
        elif choice == "5":
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    main_menu()