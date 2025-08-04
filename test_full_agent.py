"""
Test para probar el agente completo con la pregunta específica de mayo.
"""

import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

def test_full_agent_may_question():
    """Test del agente completo con la pregunta específica de mayo."""
    
    print("🧪 TESTING: Agente Completo - Pregunta de Mayo")
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
        test_question = "Cuál es el total de facturas por cobrar emitidas en mayo?"
        
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
        if "mayo" in response.lower() and "por cobrar" in response.lower():
            print("\n✅ TEST PASADO: Respuesta específica para mayo y por cobrar")
            
            # Verificar que contiene números específicos
            if any(char.isdigit() for char in response):
                print("✅ TEST PASADO: Respuesta contiene datos numéricos")
            else:
                print("❌ TEST FALLIDO: Respuesta no contiene datos numéricos")
        else:
            print("\n❌ TEST FALLIDO: Respuesta no es específica para mayo")
            
    except Exception as e:
        print(f"\n❌ ERROR EN TEST: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Función principal."""
    print("🎯 TESTING AGENTE COMPLETO")
    print("=" * 60)
    
    try:
        test_full_agent_may_question()
        
        print("\n" + "=" * 60)
        print("🎉 Test completado")
        
    except KeyboardInterrupt:
        print("\n👋 Test interrumpido")
    except Exception as e:
        print(f"\n❌ Error en test: {e}")


if __name__ == "__main__":
    main() 