#!/usr/bin/env python3
"""
Test que fuerza la retroalimentación modificando temporalmente el prompt del LLM.
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from enhanced_financial_agent_with_llm import EnhancedFinancialAgentWithLLM, FinancialAgentConfig

def test_retroalimentacion_forzada():
    print("🧪 TESTING RETROALIMENTACIÓN FORZADA")
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
    
    # Modificar temporalmente el prompt para forzar análisis adicional
    original_analyze_method = agent.llm_analyzer.analyze_with_llm
    
    def forced_analysis_method(question: str, data_summary: dict) -> str:
        """Método que fuerza la solicitud de análisis adicional."""
        if "proveedor" in question.lower() or "cliente" in question.lower():
            return "NEED_ANALYSIS: análisis detallado por proveedor y cliente"
        elif "tendencia" in question.lower() or "variacion" in question.lower():
            return "NEED_ANALYSIS: análisis de tendencias y variaciones mensuales"
        else:
            return original_analyze_method(question, data_summary)
    
    # Reemplazar temporalmente el método
    agent.llm_analyzer.analyze_with_llm = forced_analysis_method
    
    # Preguntas que deberían forzar la retroalimentación
    test_questions = [
        "cual es el proveedor con mayor monto?",
        "cual es el cliente mas importante?",
        "como varia la facturación por mes?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📋 TEST {i}: {question}")
        print(f"❓ Pregunta: {question}")
        
        try:
            response = agent.process_question(question)
            print(f"✅ Respuesta: {response[:800]}...")
            
            # Verificar si hubo retroalimentación
            if "NEED_ANALYSIS" in response or "análisis adicional" in response or "Realizando análisis adicional" in response:
                print("🔄 ✅ Se detectó retroalimentación")
            else:
                print("📋 ✅ Respuesta directa")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Restaurar el método original
    agent.llm_analyzer.analyze_with_llm = original_analyze_method
    
    print("\n🎯 TEST DE RETROALIMENTACIÓN FORZADA COMPLETADO")

if __name__ == "__main__":
    test_retroalimentacion_forzada() 