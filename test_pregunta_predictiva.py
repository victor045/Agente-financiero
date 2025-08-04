#!/usr/bin/env python3
"""
Test específico para preguntas predictivas y de análisis complejo.
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from enhanced_financial_agent_with_llm import EnhancedFinancialAgentWithLLM, FinancialAgentConfig

def test_pregunta_predictiva():
    print("🧪 TESTING PREGUNTAS PREDICTIVAS")
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
    
    # Preguntas que deberían usar LLM para análisis predictivo
    test_questions = [
        "tomando en cuenta las facturas pasadas, cual seria el proveedor con mas facturas en el futuro?",
        "cual seria la tendencia de facturación para el próximo mes?",
        "que proveedor tendra mas facturas en el futuro?",
        "como se comportara la facturación en los proximos meses?",
        "cual es el analisis de tendencias de los proveedores?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📋 TEST {i}: {question}")
        print(f"❓ Pregunta: {question}")
        
        try:
            response = agent.process_question(question)
            print(f"✅ Respuesta: {response[:800]}...")
            
            # Verificar si usó LLM
            if "LLM REAL" in response:
                print("🤖 ✅ Usó LLM para análisis predictivo")
            elif "predefinida" in response:
                print("📋 ✅ Usó respuesta predefinida")
            else:
                print("❓ Tipo de respuesta no identificado")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎯 TEST DE PREGUNTAS PREDICTIVAS COMPLETADO")

if __name__ == "__main__":
    test_pregunta_predictiva() 