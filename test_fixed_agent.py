#!/usr/bin/env python3
"""
Test simple para el agente financiero corregido.
"""

import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

from enhanced_financial_agent_fixed import EnhancedFinancialAgentFixed, FinancialAgentConfig

def test_agent():
    """Test del agente corregido."""
    print("🧪 TESTING ENHANCED FINANCIAL AGENT - FIXED VERSION")
    print("=" * 60)
    
    # Configurar agente sin visualización para testing
    config = FinancialAgentConfig(
        enable_dynamic_visualization=False,
        enable_feedback=False
    )
    
    agent = EnhancedFinancialAgentFixed(config)
    
    # Lista de preguntas para testear
    test_questions = [
        ("De las facturas por pagar cuál es la más alta?", "Factura por pagar más alta"),
        ("Cuál es el total de facturas por cobrar emitidas en mayo?", "Facturas por cobrar en mayo"),
        ("Cual fue el mes con mas facturas?", "Mes con más facturas"),
        ("Cómo variaron por mes las facturas por cobrar y por pagar? considera la fecha de emisión", "Variación mensual"),
        ("Cuál es el proveedor que mayor monto total de facturas por pagar emitió?", "Proveedor con mayor monto"),
        ("cuál es el proveedor que ha tenido la factura por pagar con los términos de pago más generosos?", "Proveedor con términos más generosos")
    ]
    
    for i, (question, description) in enumerate(test_questions, 1):
        print(f"\n📋 TEST {i}: {description}")
        print(f"❓ Pregunta: {question}")
        
        try:
            response = agent.process_question(question)
            print(f"✅ Respuesta: {response[:300]}...")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎯 TEST COMPLETADO")

if __name__ == "__main__":
    test_agent() 