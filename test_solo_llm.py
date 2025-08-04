#!/usr/bin/env python3
"""
Test para verificar que el sistema funciona correctamente usando solo LLM.
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from enhanced_financial_agent_with_llm import EnhancedFinancialAgentWithLLM, FinancialAgentConfig

def test_solo_llm():
    print("🧪 TESTING SISTEMA SOLO LLM")
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
    
    # Test de diferentes tipos de preguntas
    test_questions = [
        ("De las facturas por pagar cuál es la más alta?", "Pregunta específica"),
        ("Cuál es el total de facturas por cobrar emitidas en mayo?", "Pregunta con filtro de fecha"),
        ("Cual fue el mes con mas facturas?", "Pregunta de análisis"),
        ("Cuál es el proveedor que mayor monto total de facturas por pagar emitió?", "Pregunta de proveedores"),
        ("tomando en cuenta las facturas pasadas, cual seria el proveedor con mas facturas en el futuro?", "Pregunta predictiva"),
        ("como se comportara la facturación en los proximos meses?", "Pregunta de tendencias"),
        ("cual es el analisis de tendencias de los proveedores?", "Pregunta de análisis complejo")
    ]
    
    for i, (question, description) in enumerate(test_questions, 1):
        print(f"\n📋 TEST {i}: {description}")
        print(f"❓ Pregunta: {question}")
        
        try:
            response = agent.process_question(question)
            print(f"✅ Respuesta: {response[:800]}...")
            
            # Verificar que siempre usa LLM
            if "LLM REAL" in response:
                print("🤖 ✅ Usó LLM correctamente")
            else:
                print("❌ No usó LLM")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎯 TEST DE SISTEMA SOLO LLM FINALIZADO")

if __name__ == "__main__":
    test_solo_llm() 