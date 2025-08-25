"""
Script to populate the database with initial questions.
Run this once to add sample questions to your database.
"""
from app.database.database import SessionLocal
from app.database.crud import create_question
from app.database.models import TechArea

def seed_questions():
    """Add initial questions to the database"""
    db = SessionLocal()
    
    try:
        # JavaScript Questions
        create_question(
            db=db,
            tech_area=TechArea.JAVASCRIPT,
            difficulty="easy",
            question_text_en="What is the difference between 'let', 'const', and 'var' in JavaScript?",
            question_text_pt="Qual é a diferença entre 'let', 'const' e 'var' em JavaScript?",
            question_text_es="¿Cuál es la diferencia entre 'let', 'const' y 'var' en JavaScript?",
            expected_concepts="scope, hoisting, reassignment, block scope"
        )
        
        create_question(
            db=db,
            tech_area=TechArea.JAVASCRIPT,
            difficulty="medium",
            question_text_en="Explain how closures work in JavaScript with an example.",
            question_text_pt="Explique como funcionam as closures em JavaScript com um exemplo.",
            question_text_es="Explica cómo funcionan los closures en JavaScript con un ejemplo.",
            expected_concepts="closure, lexical scope, inner function, outer function variables"
        )
        
        # Python Questions
        create_question(
            db=db,
            tech_area=TechArea.PYTHON,
            difficulty="easy",
            question_text_en="What is the difference between a list and a tuple in Python?",
            question_text_pt="Qual é a diferença entre uma lista e uma tupla em Python?",
            question_text_es="¿Cuál es la diferencia entre una lista y una tupla en Python?",
            expected_concepts="mutability, immutability, performance, use cases"
        )
        
        create_question(
            db=db,
            tech_area=TechArea.PYTHON,
            difficulty="medium",
            question_text_en="Explain list comprehensions in Python and provide an example.",
            question_text_pt="Explique list comprehensions em Python e forneça um exemplo.",
            question_text_es="Explica las list comprehensions en Python y proporciona un ejemplo.",
            expected_concepts="list comprehension, syntax, filtering, mapping, performance"
        )
        
        # DSA Questions
        create_question(
            db=db,
            tech_area=TechArea.DSA,
            difficulty="easy",
            question_text_en="What is the time complexity of searching in a sorted array using binary search?",
            question_text_pt="Qual é a complexidade de tempo para buscar em um array ordenado usando busca binária?",
            question_text_es="¿Cuál es la complejidad temporal de buscar en un array ordenado usando búsqueda binaria?",
            expected_concepts="binary search, O(log n), divide and conquer, sorted array"
        )
        
        create_question(
            db=db,
            tech_area=TechArea.DSA,
            difficulty="medium",
            question_text_en="Explain the difference between a stack and a queue. When would you use each?",
            question_text_pt="Explique a diferença entre uma pilha (stack) e uma fila (queue). Quando você usaria cada uma?",
            question_text_es="Explica la diferencia entre una pila (stack) y una cola (queue). ¿Cuándo usarías cada una?",
            expected_concepts="LIFO, FIFO, stack operations, queue operations, use cases"
        )
        
        # Ruby Questions
        create_question(
            db=db,
            tech_area=TechArea.RUBY,
            difficulty="easy",
            question_text_en="What is the difference between a symbol and a string in Ruby?",
            question_text_pt="Qual é a diferença entre um símbolo e uma string em Ruby?",
            question_text_es="¿Cuál es la diferencia entre un símbolo y un string en Ruby?",
            expected_concepts="symbol, string, immutability, memory usage, performance"
        )
        
        print("✅ Questions seeded successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding questions: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_questions()