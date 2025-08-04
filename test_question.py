"""
Test script para probar una pregunta específica al Financial Agent.
"""

from interactive_agent import InteractiveFinancialAgent

def test_specific_question():
    """Probar una pregunta específica."""
    print("🧪 TEST: Pregunta Específica")
    print("=" * 50)
    
    # Inicializar agente
    agent = InteractiveFinancialAgent()
    
    # Pregunta de ejemplo
    question = "¿Cuál es el total de facturas emitidas?"
    
    print(f"❓ Pregunta: {question}")
    print("=" * 50)
    
    # Obtener respuesta
    response = agent.answer_question(question)
    print(response)
    
    print("\n" + "=" * 50)
    print("✅ Test completado")

if __name__ == "__main__":
    test_specific_question() 