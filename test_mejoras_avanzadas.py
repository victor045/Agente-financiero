#!/usr/bin/env python3
"""
Test para verificar las nuevas funcionalidades avanzadas del agente.
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from enhanced_financial_agent_with_llm import EnhancedFinancialAgentWithLLM, FinancialAgentConfig

def test_mejoras_avanzadas():
    print("🧪 TESTING MEJORAS AVANZADAS")
    print("=" * 60)
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️  OPENAI_API_KEY no encontrada")
        print("💡 Configura tu API key: export OPENAI_API_KEY='tu-api-key'")
        return
    
    config = FinancialAgentConfig(
        enable_llm=True,
        enable_dynamic_visualization=False,
        enable_feedback=False
    )
    
    agent = EnhancedFinancialAgentWithLLM(config)
    
    # Test 1: Memoria de conversación
    print("\n📋 TEST 1: Memoria de conversación")
    print("-" * 40)
    
    questions = [
        "Cual fue el mes con mas facturas?",
        "Y cual fue el mes con menos facturas?",
        "Comparado con mayo, como se comporto junio?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n❓ Pregunta {i}: {question}")
        try:
            response = agent.process_question(question)
            print(f"✅ Respuesta: {response[:300]}...")
            print(f"📊 Conversaciones en memoria: {len(agent.conversation_history)}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Test 2: Estadísticas de conversación
    print("\n📋 TEST 2: Estadísticas de conversación")
    print("-" * 40)
    agent.show_conversation_stats()
    
    # Test 3: Exportación de reporte
    print("\n📋 TEST 3: Exportación de reporte")
    print("-" * 40)
    result = agent.export_conversation_report("test_report.txt")
    print(f"📄 {result}")
    
    # Test 4: Limpiar historial
    print("\n📋 TEST 4: Limpiar historial")
    print("-" * 40)
    print(f"📊 Conversaciones antes de limpiar: {len(agent.conversation_history)}")
    agent.clear_conversation_history()
    print(f"📊 Conversaciones después de limpiar: {len(agent.conversation_history)}")
    
    # Test 5: Pregunta con contexto vacío
    print("\n📋 TEST 5: Pregunta con contexto vacío")
    print("-" * 40)
    try:
        response = agent.process_question("Cual es el total de facturas?")
        print(f"✅ Respuesta: {response[:300]}...")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🎯 TEST DE MEJORAS AVANZADAS FINALIZADO")

if __name__ == "__main__":
    test_mejoras_avanzadas() 