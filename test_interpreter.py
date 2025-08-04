"""
Test simple para verificar que el intérprete funciona correctamente.
"""

import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

from enhanced_financial_agent_configurable import QuestionInterpreter

def test_question_interpreter():
    """Probar el intérprete de preguntas."""
    
    test_questions = [
        "Cuál es el total de facturas por cobrar emitidas en mayo?",
        "¿Cuál es la factura por pagar más alta?",
        "¿Cuál es el total de facturas emitidas?",
        "¿Cuál es el promedio de facturas por cobrar?",
        "¿Cuáles son los gastos fijos más altos?",
        "¿Cómo está el flujo de caja?"
    ]
    
    print("🧪 TESTING QUESTION INTERPRETER")
    print("=" * 50)
    
    for question in test_questions:
        print(f"\n❓ Pregunta: {question}")
        interpretation = QuestionInterpreter.interpret_question(question)
        
        print(f"   📊 Tipo: {interpretation['question_type']}")
        print(f"   📁 Fuentes: {interpretation['data_sources']}")
        if interpretation.get('fecha_filtro'):
            print(f"   📅 Filtro fecha: {interpretation['fecha_filtro']}")
        print(f"   ❓ Aclaración necesaria: {interpretation['clarification_needed']}")
        
        if interpretation['clarification_needed']:
            print(f"   💬 Pregunta de aclaración: {interpretation['clarification_question'][:100]}...")

if __name__ == "__main__":
    test_question_interpreter() 