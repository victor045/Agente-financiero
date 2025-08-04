#!/usr/bin/env python3
"""
Test para una pregunta específica.
"""

import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

from enhanced_financial_agent_fixed import EnhancedFinancialAgentFixed, FinancialAgentConfig

def test_single_question():
    """Test de una pregunta específica."""
    print("🧪 TESTING SINGLE QUESTION")
    print("=" * 60)
    
    # Configurar agente sin visualización para testing
    config = FinancialAgentConfig(
        enable_dynamic_visualization=False,
        enable_feedback=False
    )
    
    agent = EnhancedFinancialAgentFixed(config)
    
    # Test específico
    question = "Cuál es el proveedor que mayor monto total de facturas por pagar emitió?"
    print(f"❓ Pregunta: {question}")
    
    try:
        response = agent.process_question(question)
        print(f"✅ Respuesta completa:\n{response}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_single_question() 