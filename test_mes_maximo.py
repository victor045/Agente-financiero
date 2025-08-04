"""
Test específico para verificar la interpretación de preguntas sobre "mes con más facturas".
"""

import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

def test_question_interpreter():
    """Test del intérprete para preguntas sobre mes con más facturas."""
    
    print("🧪 TESTING: Question Interpreter - Mes con más facturas")
    print("=" * 60)
    
    # Importar solo la clase QuestionInterpreter
    import enhanced_financial_agent_configurable
    QuestionInterpreter = enhanced_financial_agent_configurable.QuestionInterpreter
    
    # Preguntas de test específicas
    test_questions = [
        "cual fue el mes con mas facturas por cobrar y cual por pagar",
        "¿Cuál es el mes con más facturas por cobrar?",
        "¿Cuál es el mes con más facturas por pagar?",
        "¿Cuál es el mes con más facturas?",
        "mes con mas facturas por cobrar",
        "mes con mas facturas por pagar",
        "mes con mas facturas",
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Pregunta: {question}")
        
        try:
            interpretation = QuestionInterpreter.interpret_question(question)
            
            print(f"   📊 Tipo: {interpretation['question_type']}")
            print(f"   📁 Fuentes: {interpretation['data_sources']}")
            print(f"   📅 Filtro fecha: {interpretation.get('fecha_filtro', 'None')}")
            print(f"   ❓ Aclaración necesaria: {interpretation['clarification_needed']}")
            
            # Verificar si detectó correctamente el tipo
            expected_types = [
                "facturas_por_cobrar_mes_maximo",
                "facturas_por_pagar_mes_maximo", 
                "facturas_mes_maximo"
            ]
            
            if interpretation['question_type'] in expected_types:
                print(f"   ✅ CORRECTO: Interpretó como {interpretation['question_type']}")
            else:
                print(f"   ❌ ERROR: Esperaba un tipo de mes máximo, obtuvo {interpretation['question_type']}")
                    
        except Exception as e:
            print(f"   ❌ ERROR: {e}")


def test_full_agent():
    """Test del agente completo con preguntas sobre mes con más facturas."""
    
    print("\n🧪 TESTING: Agente Completo - Mes con más facturas")
    print("=" * 60)
    
    # Importar el agente
    import enhanced_financial_agent_configurable
    EnhancedFinancialAgentConfigurable = enhanced_financial_agent_configurable.EnhancedFinancialAgentConfigurable
    FinancialAgentConfig = enhanced_financial_agent_configurable.FinancialAgentConfig
    
    try:
        # Crear agente
        config = FinancialAgentConfig()
        agent = EnhancedFinancialAgentConfigurable(config)
        
        # Pregunta específica
        test_question = "cual fue el mes con mas facturas por cobrar y cual por pagar"
        
        print(f"❓ Pregunta: {test_question}")
        print("=" * 60)
        
        # Procesar pregunta
        response = agent.process_question(test_question)
        
        # Mostrar respuesta
        print("\n📋 RESPUESTA COMPLETA:")
        print("=" * 60)
        print(response)
        
        # Mostrar resumen
        agent.show_execution_summary()
        
        # Verificar que la respuesta es específica
        if "mes" in response.lower() and ("más" in response.lower() or "maximo" in response.lower()):
            print("\n✅ TEST PASADO: Respuesta específica sobre mes con más facturas")
        else:
            print("\n❌ TEST FALLIDO: Respuesta no es específica sobre mes con más facturas")
            
    except Exception as e:
        print(f"\n❌ ERROR EN TEST: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Función principal."""
    print("🎯 TESTING MES CON MÁS FACTURAS")
    print("=" * 60)
    
    try:
        test_question_interpreter()
        test_full_agent()
        
        print("\n" + "=" * 60)
        print("🎉 Test completado")
        
    except KeyboardInterrupt:
        print("\n👋 Test interrumpido")
    except Exception as e:
        print(f"\n❌ Error en test: {e}")


if __name__ == "__main__":
    main() 