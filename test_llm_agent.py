#!/usr/bin/env python3
"""
Test para el agente financiero con LLM.
"""

import sys
import os
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

from enhanced_financial_agent_with_llm import EnhancedFinancialAgentWithLLM, FinancialAgentConfig

def test_llm_agent():
    """Test del agente con LLM."""
    print("🧪 TESTING ENHANCED FINANCIAL AGENT WITH LLM")
    print("=" * 60)
    
    # Verificar API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️  OPENAI_API_KEY no encontrada")
        print("💡 Configura tu API key: export OPENAI_API_KEY='tu-api-key'")
        return
    
    # Configurar agente sin visualización para testing
    config = FinancialAgentConfig(
        enable_llm=True,
        enable_dynamic_visualization=False,
        enable_feedback=False
    )
    
    agent = EnhancedFinancialAgentWithLLM(config)
    
    # Lista de preguntas para testear
    test_questions = [
        ("De las facturas por pagar cuál es la más alta?", "Factura por pagar más alta"),
        ("Cuál es el total de facturas por cobrar emitidas en mayo?", "Facturas por cobrar en mayo"),
        ("Cual fue el mes con mas facturas?", "Mes con más facturas"),
        ("y cual es el mes con menos facturas?", "Mes con menos facturas - LLM"),
        ("Cómo variaron por mes las facturas por cobrar y por pagar? considera la fecha de emisión", "Variación mensual - LLM"),
        ("Cuál es el proveedor que mayor monto total de facturas por pagar emitió?", "Proveedor con mayor monto"),
        ("cuál es el proveedor que ha tenido la factura por pagar con los términos de pago más generosos?", "Proveedor con términos más generosos - LLM")
    ]
    
    for i, (question, description) in enumerate(test_questions, 1):
        print(f"\n📋 TEST {i}: {description}")
        print(f"❓ Pregunta: {question}")
        
        try:
            response = agent.process_question(question)
            print(f"✅ Respuesta: {response[:300]}...")
            
            # Verificar si usó LLM
            if "LLM REAL" in response:
                print("🤖 ✅ Usó LLM real")
            elif "predefinida" in response:
                print("📋 ✅ Usó respuesta predefinida")
            else:
                print("❓ Tipo de respuesta no identificado")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎯 TEST COMPLETADO")

if __name__ == "__main__":
    test_llm_agent() 