"""
Test simple para probar solo las funciones del agente sin ejecutar el código completo.
"""

import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

def test_question_interpreter():
    """Test específico del intérprete de preguntas."""
    
    print("🧪 TESTING: Question Interpreter")
    print("=" * 50)
    
    # Importar solo la clase QuestionInterpreter
    import enhanced_financial_agent_configurable
    QuestionInterpreter = enhanced_financial_agent_configurable.QuestionInterpreter
    
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


def test_response_formatter():
    """Test específico del formateador de respuestas."""
    
    print("\n🧪 TESTING: Response Formatter")
    print("=" * 50)
    
    # Importar solo la clase ResponseFormatter
    import enhanced_financial_agent_configurable
    ResponseFormatter = enhanced_financial_agent_configurable.ResponseFormatter
    
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


def test_data_processor():
    """Test específico del procesador de datos."""
    
    print("\n🧪 TESTING: Data Processor")
    print("=" * 50)
    
    # Importar solo las clases necesarias
    import enhanced_financial_agent_configurable
    FinancialDataProcessor = enhanced_financial_agent_configurable.FinancialDataProcessor
    FinancialAgentConfig = enhanced_financial_agent_configurable.FinancialAgentConfig
    
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


def main():
    """Función principal de testing."""
    
    print("🎯 TESTING ENHANCED FINANCIAL AGENT CONFIGURABLE")
    print("=" * 60)
    print("📋 Tests disponibles:")
    print("   1. Test del intérprete de preguntas")
    print("   2. Test del formateador de respuestas")
    print("   3. Test del procesador de datos")
    print("   4. Todos los tests")
    print("=" * 60)
    
    try:
        choice = input("\n❓ Selecciona un test (1-4): ").strip()
        
        if choice == "1":
            test_question_interpreter()
        elif choice == "2":
            test_response_formatter()
        elif choice == "3":
            test_data_processor()
        elif choice == "4":
            test_question_interpreter()
            test_response_formatter()
            test_data_processor()
        else:
            print("❌ Opción inválida")
            
    except KeyboardInterrupt:
        print("\n👋 Test interrumpido")
    except Exception as e:
        print(f"❌ Error en test: {e}")


if __name__ == "__main__":
    main() 