#!/usr/bin/env python3
"""
Test para la funcionalidad de retroalimentación del LLM.
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from enhanced_financial_agent_with_llm import EnhancedFinancialAgentWithLLM, FinancialAgentConfig

def test_retroalimentacion():
    print("🧪 TESTING RETROALIMENTACIÓN LLM")
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
    
    # Preguntas que deberían requerir análisis adicional
    test_questions = [
        "cual fue el mes con menos facturas?",
        "cual fue el mes con mas facturas?",
        "como variaron las facturas por mes?",
        "cual es el proveedor con mayor monto total?",
        "cual es el proveedor con terminos de pago mas generosos?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📋 TEST {i}: {question}")
        print(f"❓ Pregunta: {question}")
        
        try:
            response = agent.process_question(question)
            print(f"✅ Respuesta: {response[:500]}...")
            
            # Verificar si hubo retroalimentación
            if "NEED_ANALYSIS" in response or "análisis adicional" in response:
                print("🔄 ✅ Se detectó retroalimentación")
            else:
                print("📋 ✅ Respuesta directa")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎯 TEST DE RETROALIMENTACIÓN COMPLETADO")

if __name__ == "__main__":
    test_retroalimentacion() 