"""
LangGraph Studio Configuration para el Enhanced Financial Agent.
"""

import os
import subprocess
import sys
from pathlib import Path
import logging
import json

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_langgraph_config():
    """Crear configuración de LangGraph Studio."""
    config = {
        "dockerfile_lines": [],
        "graphs": {
            "Enhanced Financial Agent": "./financial_agent/enhanced_financial_agent.py:create_enhanced_financial_agent"
        },
        "python_version": "3.11",
        "env": "./.env",
        "dependencies": [
            "."
        ],
        "auth": {
            "path": "./src/security/auth.py:auth"
        }
    }
    
    # Guardar configuración
    with open('langgraph_enhanced.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuración de LangGraph Studio creada: langgraph_enhanced.json")
    return config


def create_graph_export():
    """Crear archivo de exportación del grafo."""
    export_file = "financial_agent/enhanced_agent_export.py"
    
    export_content = '''
"""
Enhanced Financial Agent - Export para LangGraph Studio.
"""

from enhanced_financial_agent import create_enhanced_financial_agent

# Exportar el grafo para LangGraph Studio
enhanced_financial_agent = create_enhanced_financial_agent()

if __name__ == "__main__":
    print("🎯 Enhanced Financial Agent - LangGraph Studio Export")
    print("✅ Grafo exportado correctamente")
'''
    
    with open(export_file, 'w') as f:
        f.write(export_content)
    
    print(f"✅ Archivo de exportación creado: {export_file}")
    return export_file


def check_langgraph_cli():
    """Verificar si langgraph-cli está instalado."""
    try:
        result = subprocess.run(['langgraph', '--version'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def install_langgraph_cli():
    """Instalar langgraph-cli si no está disponible."""
    try:
        print("📦 Instalando langgraph-cli...")
        subprocess.run(['pip', 'install', 'langgraph-cli[inmem]'], 
                      check=True, capture_output=True)
        print("✅ langgraph-cli instalado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando langgraph-cli: {e}")
        return False


def run_langgraph_studio():
    """Ejecutar LangGraph Studio con el agente mejorado."""
    if not check_langgraph_cli():
        print("⚠️  langgraph-cli no encontrado")
        if not install_langgraph_cli():
            print("❌ No se pudo instalar langgraph-cli")
            return False
    
    try:
        print("🚀 Iniciando LangGraph Studio...")
        print("📋 URLs disponibles:")
        print("   🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024")
        print("   📚 API Docs: http://127.0.0.1:2024/docs")
        print("   🚀 API: http://127.0.0.1:2024")
        print("\n⏳ Iniciando servidor...")
        
        # Ejecutar LangGraph Studio
        subprocess.run(['langgraph', 'dev', '--allow-blocking'], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando LangGraph Studio: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 LangGraph Studio detenido")
        return True


def show_enhanced_features():
    """Mostrar características del agente mejorado."""
    print("🎯 ENHANCED FINANCIAL AGENT - CARACTERÍSTICAS")
    print("=" * 60)
    
    print("\n📊 MEJORAS BASADAS EN OPEN_DEEP_RESEARCH:")
    print("   ✅ Estado estructurado con Pydantic")
    print("   ✅ Configuración centralizada")
    print("   ✅ Procesamiento robusto de datos")
    print("   ✅ Análisis financiero especializado")
    print("   ✅ Respuestas estructuradas")
    print("   ✅ Manejo de errores avanzado")
    print("   ✅ Visualización en tiempo real")
    print("   ✅ Monitoreo de ejecución")
    
    print("\n🔧 NODOS DEL GRAFO:")
    print("   📝 interpret_question: Interpretar preguntas financieras")
    print("   🔍 select_data_sources: Seleccionar fuentes de datos")
    print("   📊 load_and_analyze: Cargar y analizar datos")
    print("   📋 format_response: Formatear respuesta ejecutiva")
    print("   ❓ clarify_question: Solicitar aclaraciones")
    
    print("\n📈 TIPOS DE ANÁLISIS:")
    print("   💰 facturas_por_pagar_max: Factura por pagar más alta")
    print("   💰 facturas_por_cobrar_max: Factura por cobrar más alta")
    print("   📊 facturas_total: Total de facturas emitidas")
    print("   📊 facturas_promedio: Promedio de facturas")
    print("   💸 gastos_analisis: Análisis de gastos fijos")
    print("   💳 flujo_caja: Análisis de flujo de caja")
    print("   📋 general: Análisis general")
    
    print("\n🎨 VISUALIZACIÓN:")
    print("   🌐 LangGraph Studio: Visualización interactiva")
    print("   📊 matplotlib: Gráficos estáticos y animados")
    print("   📝 Consola: Progreso en tiempo real")
    print("   📋 Logs: Trazabilidad completa")


def create_demo_questions():
    """Crear archivo con preguntas de demostración."""
    demo_file = "financial_agent/demo_questions.json"
    
    questions = [
        {
            "id": 1,
            "question": "¿Cuál es la factura por pagar más alta?",
            "type": "facturas_por_pagar_max",
            "expected_files": ["facturas.xlsx"],
            "description": "Encuentra la factura con el monto más alto por pagar"
        },
        {
            "id": 2,
            "question": "¿Cuál es la factura por cobrar más alta?",
            "type": "facturas_por_cobrar_max",
            "expected_files": ["facturas.xlsx"],
            "description": "Encuentra la factura con el monto más alto por cobrar"
        },
        {
            "id": 3,
            "question": "¿Cuál es el total de facturas emitidas?",
            "type": "facturas_total",
            "expected_files": ["facturas.xlsx"],
            "description": "Calcula el monto total de todas las facturas"
        },
        {
            "id": 4,
            "question": "¿Cuál es el promedio de facturas por cobrar?",
            "type": "facturas_promedio",
            "expected_files": ["facturas.xlsx"],
            "description": "Calcula el promedio de facturas por cobrar"
        },
        {
            "id": 5,
            "question": "¿Cuáles son los gastos fijos más altos?",
            "type": "gastos_analisis",
            "expected_files": ["gastos_fijos.xlsx"],
            "description": "Analiza los gastos fijos por categoría"
        },
        {
            "id": 6,
            "question": "¿Cómo está el flujo de caja?",
            "type": "flujo_caja",
            "expected_files": ["Estado_cuenta.xlsx"],
            "description": "Analiza el flujo de caja y movimientos"
        }
    ]
    
    with open(demo_file, 'w') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Preguntas de demostración creadas: {demo_file}")
    return demo_file


def show_studio_instructions():
    """Mostrar instrucciones para usar LangGraph Studio."""
    print("🎯 LANGGRAPH STUDIO - INSTRUCCIONES")
    print("=" * 60)
    
    print("\n📋 PASOS PARA USAR LANGGRAPH STUDIO:")
    print("1. Ejecutar el servidor:")
    print("   python3 financial_agent/langgraph_studio_enhanced.py")
    
    print("\n2. Abrir el navegador en:")
    print("   https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024")
    
    print("\n3. En Studio, podrás:")
    print("   🔍 Ver el grafo visualmente")
    print("   🧪 Probar cada nodo individualmente")
    print("   📊 Ver el flujo de datos")
    print("   🔧 Depurar el comportamiento")
    print("   📈 Monitorear ejecuciones")
    print("   📋 Ver el estado en tiempo real")
    
    print("\n🎨 CARACTERÍSTICAS DE STUDIO:")
    print("   ✅ Visualización interactiva del grafo")
    print("   ✅ Testing de nodos individuales")
    print("   ✅ Monitoreo de ejecuciones en tiempo real")
    print("   ✅ Debugging de errores")
    print("   ✅ Exportación de resultados")
    print("   ✅ Análisis de rendimiento")
    
    print("\n🔧 CONFIGURACIÓN AVANZADA:")
    print("   - Modificar prompts en tiempo real")
    print("   - Ajustar parámetros del modelo")
    print("   - Ver logs detallados")
    print("   - Exportar configuraciones")
    print("   - Analizar métricas de ejecución")


def main():
    """Función principal para LangGraph Studio Enhanced."""
    print("🎯 ENHANCED FINANCIAL AGENT - LANGGRAPH STUDIO")
    print("=" * 60)
    
    try:
        # Crear configuración
        create_langgraph_config()
        
        # Crear exportación del grafo
        create_graph_export()
        
        # Crear preguntas de demostración
        create_demo_questions()
        
        # Mostrar características
        show_enhanced_features()
        
        print("\n" + "=" * 60)
        
        # Mostrar instrucciones
        show_studio_instructions()
        
        print("\n" + "=" * 60)
        
        # Preguntar si ejecutar Studio
        response = input("\n❓ ¿Deseas iniciar LangGraph Studio ahora? (s/n): ").strip().lower()
        
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            run_langgraph_studio()
        else:
            print("💡 Para iniciar Studio más tarde, ejecuta:")
            print("   python3 financial_agent/langgraph_studio_enhanced.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Error en main: {e}")


if __name__ == "__main__":
    main() 