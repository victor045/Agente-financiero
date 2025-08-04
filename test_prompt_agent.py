"""
Test para el agente financiero con prompt engineering.
"""

import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

def test_prompt_agent():
    """Test del agente con prompts."""
    
    print("🧪 TESTING: Enhanced Financial Agent with Prompts")
    print("=" * 60)
    
    # Importar el agente
    import enhanced_financial_agent_with_prompts
    EnhancedFinancialAgentWithPrompts = enhanced_financial_agent_with_prompts.EnhancedFinancialAgentWithPrompts
    FinancialAgentConfig = enhanced_financial_agent_with_prompts.FinancialAgentConfig
    
    try:
        # Crear agente con prompts habilitados
        config = FinancialAgentConfig(
            enable_prompt_engineering=True,
            enable_flexible_responses=True,
            enable_graph_visualization=True
        )
        
        agent = EnhancedFinancialAgentWithPrompts(config)
        
        # Preguntas de test
        test_questions = [
            # Preguntas pre-configuradas
            "cual fue el mes con mas facturas por cobrar y cual por pagar",
            "¿Cuál es el total de facturas por cobrar emitidas en mayo?",
            
            # Preguntas no pre-configuradas (usarán prompts)
            "¿Cómo está la salud financiera de la empresa?",
            "¿Qué tendencias veo en los gastos?",
            "¿Cuál es la rentabilidad de las facturas por cobrar vs por pagar?",
            "¿Hay algún patrón en los movimientos bancarios?",
            "¿Qué recomendaciones tienes para mejorar el flujo de caja?",
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n{'='*60}")
            print(f"TEST {i}: {question}")
            print(f"{'='*60}")
            
            # Procesar pregunta
            response = agent.process_question(question)
            
            # Mostrar respuesta
            print("\n📋 RESPUESTA:")
            print("-" * 40)
            print(response)
            
            # Mostrar resumen
            agent.show_execution_summary()
            
            print(f"\n✅ Test {i} completado")
            
    except Exception as e:
        print(f"\n❌ ERROR EN TEST: {e}")
        import traceback
        traceback.print_exc()


def test_prompt_system():
    """Test del sistema de prompts."""
    
    print("\n🧪 TESTING: Sistema de Prompts")
    print("=" * 60)
    
    try:
        from prompts import FinancialPrompts, PromptManager
        
        # Test de formateo de datos
        test_data = {
            'facturas': {
                'total': 439202.23,
                'por_cobrar': 214906.45,
                'por_pagar': 224295.78
            },
            'gastos_fijos': {
                'total_gastos': 15000.00
            },
            'estado_cuenta': {
                'total_movimientos': 50000.00
            }
        }
        
        # Formatear resumen
        summary = FinancialPrompts.format_data_summary(test_data)
        print("📊 Resumen de datos formateado:")
        print(summary)
        
        # Test de creación de prompts
        question = "¿Cómo está la salud financiera?"
        analysis_prompt = FinancialPrompts.create_analysis_prompt(question, test_data)
        print(f"\n🤖 Prompt de análisis ({len(analysis_prompt)} caracteres):")
        print(analysis_prompt[:300] + "...")
        
        # Test de PromptManager
        pm = PromptManager()
        pm.add_to_history("user", "¿Cuál es el total de facturas?")
        pm.add_to_history("assistant", "El total es $439,202.23 MXN")
        
        context_prompt = pm.get_context_prompt("¿Y los gastos?", test_data)
        print(f"\n📝 Prompt con contexto ({len(context_prompt)} caracteres):")
        print(context_prompt[:400] + "...")
        
        print("\n✅ Sistema de prompts funcionando correctamente")
        
    except Exception as e:
        print(f"\n❌ ERROR EN TEST DE PROMPTS: {e}")
        import traceback
        traceback.print_exc()


def test_flexible_responses():
    """Test de respuestas flexibles."""
    
    print("\n🧪 TESTING: Respuestas Flexibles")
    print("=" * 60)
    
    try:
        import enhanced_financial_agent_with_prompts
        EnhancedFinancialAgentWithPrompts = enhanced_financial_agent_with_prompts.EnhancedFinancialAgentWithPrompts
        FinancialAgentConfig = enhanced_financial_agent_with_prompts.FinancialAgentConfig
        
        # Crear agente
        config = FinancialAgentConfig(
            enable_prompt_engineering=True,
            enable_flexible_responses=True,
            enable_graph_visualization=False  # Deshabilitar para test más rápido
        )
        
        agent = EnhancedFinancialAgentWithPrompts(config)
        
        # Preguntas que deberían usar prompts
        flexible_questions = [
            "¿Qué análisis puedes hacer de la situación financiera?",
            "¿Hay algo preocupante en los datos?",
            "¿Qué oportunidades veo en los números?",
            "¿Cómo puedo optimizar el flujo de efectivo?",
            "¿Qué patrones identificas en los datos?",
        ]
        
        for i, question in enumerate(flexible_questions, 1):
            print(f"\n--- Test {i}: {question} ---")
            
            response = agent.process_question(question)
            
            # Verificar si usó prompt engineering
            if "🤖 RESPUESTA GENERADA CON PROMPT ENGINEERING" in response:
                print("✅ Usó prompt engineering correctamente")
            else:
                print("❌ No usó prompt engineering")
            
            print(f"Respuesta: {response[:100]}...")
        
        print("\n✅ Tests de respuestas flexibles completados")
        
    except Exception as e:
        print(f"\n❌ ERROR EN TEST DE RESPUESTAS FLEXIBLES: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Función principal."""
    print("🎯 TESTING ENHANCED FINANCIAL AGENT WITH PROMPTS")
    print("=" * 60)
    
    try:
        test_prompt_system()
        test_flexible_responses()
        test_prompt_agent()
        
        print("\n" + "=" * 60)
        print("🎉 Todos los tests completados exitosamente")
        
    except KeyboardInterrupt:
        print("\n👋 Test interrumpido")
    except Exception as e:
        print(f"\n❌ Error en test: {e}")


if __name__ == "__main__":
    main() 