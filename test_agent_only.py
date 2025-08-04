"""
Test file para probar solo la función del agente sin ejecutar el código completo.
"""

import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

# Importar solo las clases necesarias del agente configurable
# Evitar ejecutar el main() del agente
import enhanced_financial_agent_configurable as agent_module

# Obtener las clases sin ejecutar main()
EnhancedFinancialAgentConfigurable = agent_module.EnhancedFinancialAgentConfigurable
FinancialAgentConfig = agent_module.FinancialAgentConfig


def test_specific_question():
    """Test específico para la pregunta de facturas por cobrar en mayo."""
    
    print("🧪 TESTING: Agente Configurable")
    print("=" * 50)
    
    # Crear agente
    config = FinancialAgentConfig()
    agent = EnhancedFinancialAgentConfigurable(config)
    
    # Pregunta específica a testear
    test_question = "Cuál es el total de facturas por cobrar emitidas en mayo?"
    
    print(f"❓ Pregunta de test: {test_question}")
    print("=" * 50)
    
    try:
        # Procesar la pregunta
        response = agent.process_question(test_question)
        
        # Mostrar respuesta
        print("\n📋 RESPUESTA DEL AGENTE:")
        print("=" * 50)
        print(response)
        
        # Mostrar resumen de ejecución
        agent.show_execution_summary()
        
        # Verificar si la respuesta contiene información específica de mayo
        if "mayo" in response.lower() and "por cobrar" in response.lower():
            print("\n✅ TEST PASADO: La respuesta incluye información específica de mayo y por cobrar")
        else:
            print("\n❌ TEST FALLIDO: La respuesta no incluye información específica de mayo")
            
    except Exception as e:
        print(f"\n❌ ERROR EN TEST: {e}")


def test_question_interpreter():
    """Test específico del intérprete de preguntas."""
    
    print("\n🧪 TESTING: Question Interpreter")
    print("=" * 50)
    
    from enhanced_financial_agent_configurable import QuestionInterpreter
    
    # Preguntas de test
    test_questions = [
        "Cuál es el total de facturas por cobrar emitidas en mayo?",
        "¿Cuál es la factura por pagar más alta?",
        "¿Cuál es el total de facturas emitidas?",
        "test",  # Pregunta corta que debería pedir aclaración
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Pregunta: {question}")
        
        try:
            interpretation = QuestionInterpreter.interpret_question(question)
            
            print(f"   📊 Tipo: {interpretation['question_type']}")
            print(f"   📁 Fuentes: {interpretation['data_sources']}")
            print(f"   📅 Filtro fecha: {interpretation.get('fecha_filtro', 'None')}")
            print(f"   ❓ Aclaración necesaria: {interpretation['clarification_needed']}")
            
            # Verificar específicamente la pregunta de mayo
            if "mayo" in question.lower():
                expected_type = "facturas_por_cobrar_total_fecha"
                if interpretation['question_type'] == expected_type:
                    print(f"   ✅ CORRECTO: Interpretó como {expected_type}")
                else:
                    print(f"   ❌ ERROR: Esperaba {expected_type}, obtuvo {interpretation['question_type']}")
                    
        except Exception as e:
            print(f"   ❌ ERROR: {e}")


def test_data_processor():
    """Test específico del procesador de datos."""
    
    print("\n🧪 TESTING: Data Processor")
    print("=" * 50)
    
    from enhanced_financial_agent_configurable import FinancialDataProcessor, FinancialAgentConfig
    
    try:
        # Crear procesador
        config = FinancialAgentConfig()
        processor = FinancialDataProcessor(config)
        
        # Cargar datos
        print("📊 Cargando datos...")
        data = processor.load_all_data()
        
        print(f"✅ Datos cargados: {list(data.keys())}")
        
        # Testear análisis con filtro de fecha
        if 'facturas' in data:
            print("\n📅 Testeando análisis con filtro de fecha...")
            analysis = processor.analyze_facturas("mayo")
            
            print(f"📊 Análisis de mayo:")
            print(f"   - Filtro aplicado: {analysis.get('fecha_filtro', 'None')}")
            print(f"   - Registros filtrados: {analysis.get('registros_filtrados', 0)}")
            print(f"   - Por cobrar: ${analysis.get('por_cobrar', 0):,.2f}")
            print(f"   - Por pagar: ${analysis.get('por_pagar', 0):,.2f}")
            
            if analysis.get('fecha_filtro') == "mayo":
                print("   ✅ Filtro de fecha aplicado correctamente")
            else:
                print("   ❌ Filtro de fecha no aplicado")
        else:
            print("❌ No se encontraron datos de facturas")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")


def test_response_formatter():
    """Test específico del formateador de respuestas."""
    
    print("\n🧪 TESTING: Response Formatter")
    print("=" * 50)
    
    from enhanced_financial_agent_configurable import ResponseFormatter
    
    # Datos de prueba
    test_analysis = {
        'por_cobrar': 121000.0,
        'por_cobrar_count': 12,
        'por_cobrar_promedio': 10083.33,
        'fecha_filtro': 'mayo',
        'registros_filtrados': 12
    }
    
    test_question = "Cuál es el total de facturas por cobrar emitidas en mayo?"
    test_type = "facturas_por_cobrar_total_fecha"
    
    try:
        response = ResponseFormatter.format_response(test_question, test_analysis, test_type)
        
        print("📋 Respuesta formateada:")
        print(response)
        
        # Verificar que la respuesta contiene la información esperada
        if "mayo" in response and "121,000" in response and "12" in response:
            print("✅ TEST PASADO: Respuesta contiene información correcta de mayo")
        else:
            print("❌ TEST FALLIDO: Respuesta no contiene información correcta")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")


def main():
    """Función principal de testing."""
    
    print("🎯 TESTING ENHANCED FINANCIAL AGENT CONFIGURABLE")
    print("=" * 60)
    print("📋 Tests disponibles:")
    print("   1. Test específico de pregunta de mayo")
    print("   2. Test del intérprete de preguntas")
    print("   3. Test del procesador de datos")
    print("   4. Test del formateador de respuestas")
    print("   5. Todos los tests")
    print("=" * 60)
    
    try:
        choice = input("\n❓ Selecciona un test (1-5): ").strip()
        
        if choice == "1":
            test_specific_question()
        elif choice == "2":
            test_question_interpreter()
        elif choice == "3":
            test_data_processor()
        elif choice == "4":
            test_response_formatter()
        elif choice == "5":
            test_specific_question()
            test_question_interpreter()
            test_data_processor()
            test_response_formatter()
        else:
            print("❌ Opción inválida")
            
    except KeyboardInterrupt:
        print("\n👋 Test interrumpido")
    except Exception as e:
        print(f"❌ Error en test: {e}")


if __name__ == "__main__":
    main() 