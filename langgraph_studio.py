"""
LangGraph Studio - Visualización interactiva del Financial Agent.
"""

import os
import subprocess
import sys
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    print("📦 Instalando langgraph-cli...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "langgraph-cli[inmem]"
        ])
        print("✅ langgraph-cli instalado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando langgraph-cli: {e}")
        return False


def create_studio_config():
    """Crear configuración para LangGraph Studio."""
    config_content = """
# LangGraph Studio Configuration
# Archivo de configuración para el Financial Agent

# Configuración del grafo
graph_name: "Financial Agent"
graph_description: "Agente conversacional para análisis financiero"

# Configuración del servidor
host: "127.0.0.1"
port: 8123

# Configuración de desarrollo
dev_mode: true
allow_blocking: true

# Configuración de logging
log_level: "INFO"
"""
    
    config_file = Path("langgraph_studio_config.yaml")
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    print(f"✅ Configuración guardada en {config_file}")
    return config_file


def run_langgraph_studio():
    """Ejecutar LangGraph Studio."""
    print("🚀 Iniciando LangGraph Studio...")
    
    # Verificar instalación
    if not check_langgraph_cli():
        if not install_langgraph_cli():
            print("❌ No se pudo instalar langgraph-cli")
            return False
    
    # Crear configuración
    config_file = create_studio_config()
    
    try:
        # Ejecutar LangGraph Studio
        print("🌐 Iniciando servidor de LangGraph Studio...")
        print("📱 URLs disponibles:")
        print("   - Studio UI: http://127.0.0.1:8123")
        print("   - API Docs: http://127.0.0.1:8123/docs")
        print("   - Graph UI: http://127.0.0.1:8123/graph")
        print("\n💡 Presiona Ctrl+C para detener el servidor")
        
        # Comando para ejecutar el grafo
        cmd = [
            "langgraph", "dev",
            "--allow-blocking",
            "--port", "8123",
            "--host", "127.0.0.1"
        ]
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error ejecutando LangGraph Studio: {e}")
        return False
    
    return True


def create_graph_export():
    """Crear exportación del grafo para Studio."""
    export_content = """
# Financial Agent Graph Export
# Para usar en LangGraph Studio

from financial_agent.agent import create_financial_agent

# Crear el grafo
graph = create_financial_agent()

# Configuración para Studio
config = {
    "graph_name": "Financial Agent",
    "description": "Agente conversacional para análisis financiero",
    "version": "1.0.0",
    "tags": ["financial", "analysis", "conversational"]
}

# Exportar para Studio
if __name__ == "__main__":
    # El grafo está listo para usar en Studio
    print("✅ Financial Agent Graph exportado para LangGraph Studio")
    print("🎯 Nodos disponibles:")
    print("   - interpret_question")
    print("   - select_data_sources") 
    print("   - load_and_analyze")
    print("   - format_response")
"""
    
    export_file = Path("financial_agent_studio_export.py")
    with open(export_file, 'w') as f:
        f.write(export_content)
    
    print(f"✅ Exportación del grafo guardada en {export_file}")
    return export_file


def show_studio_instructions():
    """Mostrar instrucciones para usar LangGraph Studio."""
    print("🎯 LANGGRAPH STUDIO - INSTRUCCIONES")
    print("=" * 60)
    
    print("\n📋 PASOS PARA USAR LANGGRAPH STUDIO:")
    print("1. Ejecutar el servidor:")
    print("   python3 financial_agent/langgraph_studio.py")
    
    print("\n2. Abrir el navegador en:")
    print("   http://127.0.0.1:8123")
    
    print("\n3. En Studio, podrás:")
    print("   🔍 Ver el grafo visualmente")
    print("   🧪 Probar cada nodo individualmente")
    print("   📊 Ver el flujo de datos")
    print("   🔧 Depurar el comportamiento")
    print("   📈 Monitorear ejecuciones")
    
    print("\n🎨 CARACTERÍSTICAS DE STUDIO:")
    print("   ✅ Visualización interactiva del grafo")
    print("   ✅ Testing de nodos individuales")
    print("   ✅ Monitoreo de ejecuciones en tiempo real")
    print("   ✅ Debugging de errores")
    print("   ✅ Exportación de resultados")
    
    print("\n🔧 CONFIGURACIÓN AVANZADA:")
    print("   - Modificar prompts en tiempo real")
    print("   - Ajustar parámetros del modelo")
    print("   - Ver logs detallados")
    print("   - Exportar configuraciones")


def main():
    """Función principal para LangGraph Studio."""
    print("🎯 LANGGRAPH STUDIO - FINANCIAL AGENT")
    print("=" * 60)
    
    try:
        # Crear exportación del grafo
        create_graph_export()
        
        print("\n" + "=" * 60)
        
        # Mostrar instrucciones
        show_studio_instructions()
        
        print("\n" + "=" * 60)
        
        # Preguntar si ejecutar Studio
        response = input("\n❓ ¿Quieres iniciar LangGraph Studio ahora? (s/n): ").strip().lower()
        
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            run_langgraph_studio()
        else:
            print("💡 Para iniciar Studio más tarde, ejecuta:")
            print("   python3 financial_agent/langgraph_studio.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main() 