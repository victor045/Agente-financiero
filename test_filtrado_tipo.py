#!/usr/bin/env python3
"""
Test específico para verificar el filtrado por tipo de facturas.
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from enhanced_financial_agent_with_llm import EnhancedFinancialAgentWithLLM, FinancialAgentConfig

def test_filtrado_tipo():
    print("🧪 TESTING FILTRADO POR TIPO")
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
    
    # Test 1: Facturas por cobrar en mayo
    print("\n📋 TEST 1: Facturas por cobrar en mayo")
    print("-" * 40)
    
    try:
        response = agent.process_question("¿Cuánto se facturó en mayo por facturas por cobrar?")
        print(f"✅ Respuesta: {response[:500]}...")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Facturas por pagar en mayo
    print("\n📋 TEST 2: Facturas por pagar en mayo")
    print("-" * 40)
    
    try:
        response = agent.process_question("¿Cuánto se facturó en mayo por facturas por pagar?")
        print(f"✅ Respuesta: {response[:500]}...")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Total general en mayo
    print("\n📋 TEST 3: Total general en mayo")
    print("-" * 40)
    
    try:
        response = agent.process_question("¿Cuánto se facturó en mayo en total?")
        print(f"✅ Respuesta: {response[:500]}...")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Comparación por tipo
    print("\n📋 TEST 4: Comparación por tipo")
    print("-" * 40)
    
    try:
        response = agent.process_question("¿Cómo se comparan las facturas por cobrar vs por pagar en mayo?")
        print(f"✅ Respuesta: {response[:500]}...")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🎯 TEST DE FILTRADO POR TIPO FINALIZADO")

if __name__ == "__main__":
    test_filtrado_tipo() 