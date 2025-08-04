#!/usr/bin/env python3
"""
Test específico para la pregunta que falló.
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from enhanced_financial_agent_with_llm import EnhancedFinancialAgentWithLLM, FinancialAgentConfig

def test_pregunta_especifica():
    print("🧪 TESTING PREGUNTA ESPECÍFICA")
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
    
    # La pregunta específica que falló
    question = "tomando en cuenta las facturas pasadas, cual seria el proveedor con mas facturas en el futuro?"
    
    print(f"❓ Pregunta: {question}")
    
    try:
        response = agent.process_question(question)
        print(f"✅ Respuesta: {response[:1000]}...")
        
        # Verificar si usó LLM
        if "LLM REAL" in response:
            print("🤖 ✅ Usó LLM para análisis predictivo")
        elif "predefinida" in response:
            print("📋 ✅ Usó respuesta predefinida")
        else:
            print("❓ Tipo de respuesta no identificado")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🎯 TEST DE PREGUNTA ESPECÍFICA COMPLETADO")

if __name__ == "__main__":
    test_pregunta_especifica() 