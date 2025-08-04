#!/usr/bin/env python3
"""
Test completo para verificar todas las mejoras implementadas.
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from enhanced_financial_agent_with_llm import EnhancedFinancialAgentWithLLM, FinancialAgentConfig

def test_mejoras_completas():
    print("🧪 TESTING MEJORAS COMPLETAS")
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
    
    # Test de respuestas predefinidas mejoradas
    predefined_questions = [
        ("De las facturas por pagar cuál es la más alta?", "Factura por pagar más alta"),
        ("Cuál es el total de facturas por cobrar emitidas en mayo?", "Facturas por cobrar en mayo"),
        ("Cual fue el mes con mas facturas?", "Mes con más facturas"),
        ("Cuál es el proveedor que mayor monto total de facturas por pagar emitió?", "Proveedor con mayor monto")
    ]
    
    print("\n📋 TESTING RESPUESTAS PREDEFINIDAS MEJORADAS")
    print("-" * 50)
    
    for i, (question, description) in enumerate(predefined_questions, 1):
        print(f"\n📋 TEST {i}: {description}")
        print(f"❓ Pregunta: {question}")
        
        try:
            response = agent.process_question(question)
            print(f"✅ Respuesta: {response[:600]}...")
            
            # Verificar si tiene análisis específico
            if "Detailed Analysis" in response and "Executive Summary" in response:
                print("📊 ✅ Respuesta con análisis específico")
            else:
                print("❌ Respuesta genérica")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Test de preguntas predictivas mejoradas
    predictive_questions = [
        ("tomando en cuenta las facturas pasadas, cual seria el proveedor con mas facturas en el futuro?", "Análisis predictivo de proveedores"),
        ("cual seria la tendencia de facturación para el próximo mes?", "Tendencia de facturación"),
        ("como se comportara la facturación en los proximos meses?", "Comportamiento futuro")
    ]
    
    print("\n📋 TESTING PREGUNTAS PREDICTIVAS MEJORADAS")
    print("-" * 50)
    
    for i, (question, description) in enumerate(predictive_questions, 1):
        print(f"\n📋 TEST {i}: {description}")
        print(f"❓ Pregunta: {question}")
        
        try:
            response = agent.process_question(question)
            print(f"✅ Respuesta: {response[:800]}...")
            
            # Verificar si usó LLM
            if "LLM REAL" in response:
                print("🤖 ✅ Usó LLM para análisis predictivo")
            else:
                print("📋 ✅ Usó respuesta predefinida")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎯 TEST DE MEJORAS COMPLETAS FINALIZADO")

if __name__ == "__main__":
    test_mejoras_completas() 