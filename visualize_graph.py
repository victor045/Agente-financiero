"""
Visualización del grafo LangGraph para el Financial Agent.
"""

import sys
import os
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

try:
    import matplotlib.pyplot as plt
    import networkx as nx
    from agent import create_financial_agent
    import logging
except ImportError as e:
    print(f"⚠️  Error de importación: {e}")
    print("💡 Instala las dependencias: pip install matplotlib networkx")
    sys.exit(1)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_graph_visualization():
    """Crear visualización del grafo LangGraph."""
    
    try:
        # Crear el grafo
        workflow = create_financial_agent()
        
        # Crear grafo NetworkX para visualización
        G = nx.DiGraph()
        
        # Nodos del grafo
        nodes = [
            "interpret_question",
            "select_data_sources", 
            "load_and_analyze",
            "format_response",
            "END"
        ]
        
        # Agregar nodos
        for node in nodes:
            G.add_node(node)
        
        # Agregar edges (conexiones)
        edges = [
            ("interpret_question", "select_data_sources"),
            ("select_data_sources", "load_and_analyze"),
            ("load_and_analyze", "format_response"),
            ("format_response", "END")
        ]
        
        for edge in edges:
            G.add_edge(edge[0], edge[1])
        
        return G
        
    except Exception as e:
        print(f"❌ Error creando visualización: {e}")
        return None


def visualize_graph_interactive():
    """Visualización interactiva del grafo."""
    G = create_graph_visualization()
    
    if G is None:
        print("❌ No se pudo crear el grafo para visualización")
        return
    
    # Configurar el layout
    pos = nx.spring_layout(G, k=3, iterations=50)
    
    # Crear figura
    plt.figure(figsize=(12, 8))
    
    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, 
                          node_color=['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightgray'],
                          node_size=3000,
                          alpha=0.8)
    
    # Dibujar edges
    nx.draw_networkx_edges(G, pos, 
                          edge_color='gray',
                          arrows=True,
                          arrowsize=20,
                          arrowstyle='->',
                          width=2)
    
    # Agregar etiquetas
    labels = {
        'interpret_question': 'Interpretar\nPregunta',
        'select_data_sources': 'Seleccionar\nFuentes de Datos',
        'load_and_analyze': 'Cargar y\nAnalizar',
        'format_response': 'Formatear\nRespuesta',
        'END': 'FIN'
    }
    
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight='bold')
    
    # Configurar título y layout
    plt.title("🎯 Financial Agent - Flujo de Trabajo LangGraph", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    
    # Guardar imagen
    plt.savefig('financial_agent_workflow.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfico guardado como 'financial_agent_workflow.png'")
    
    # Mostrar gráfico
    plt.show()


def visualize_graph_text():
    """Visualización en texto del grafo."""
    G = create_graph_visualization()
    
    if G is None:
        print("❌ No se pudo crear el grafo para visualización")
        return
    
    print("🎯 FINANCIAL AGENT - VISUALIZACIÓN DEL GRAFO")
    print("=" * 60)
    
    print("\n📊 NODOS DEL GRAFO:")
    for i, node in enumerate(G.nodes(), 1):
        print(f"  {i}. {node}")
    
    print("\n🔗 CONEXIONES (EDGES):")
    for i, edge in enumerate(G.edges(), 1):
        print(f"  {i}. {edge[0]} → {edge[1]}")
    
    print("\n📈 FLUJO DE TRABAJO:")
    print("  1. interpret_question → Interpreta la pregunta del usuario")
    print("  2. select_data_sources → Selecciona archivos Excel relevantes")
    print("  3. load_and_analyze → Carga datos y realiza análisis financiero")
    print("  4. format_response → Formatea la respuesta final")
    print("  5. END → Termina el proceso")
    
    print("\n🎨 TIPOS DE NODOS:")
    print("  🔵 interpret_question: Análisis de lenguaje natural")
    print("  🟢 select_data_sources: Selección inteligente de datos")
    print("  🔴 load_and_analyze: Procesamiento y análisis")
    print("  🟡 format_response: Formateo de respuesta")
    print("  ⚫ END: Punto de terminación")


def visualize_graph_mermaid():
    """Generar diagrama Mermaid del grafo."""
    mermaid_code = """
```mermaid
graph TD
    A[interpret_question<br/>Interpretar Pregunta] --> B[select_data_sources<br/>Seleccionar Fuentes]
    B --> C[load_and_analyze<br/>Cargar y Analizar]
    C --> D[format_response<br/>Formatear Respuesta]
    D --> E[END<br/>Terminar]
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#fff3e0
    style D fill:#e8f5e8
    style E fill:#f5f5f5
```
"""
    
    print("🎯 FINANCIAL AGENT - DIAGRAMA MERMAID")
    print("=" * 60)
    print(mermaid_code)
    
    # Guardar en archivo
    with open('financial_agent_mermaid.md', 'w') as f:
        f.write("# Financial Agent - Diagrama Mermaid\n\n")
        f.write(mermaid_code)
    
    print("✅ Diagrama Mermaid guardado como 'financial_agent_mermaid.md'")


def visualize_graph_detailed():
    """Visualización detallada con información de cada nodo."""
    print("🎯 FINANCIAL AGENT - ANÁLISIS DETALLADO DEL GRAFO")
    print("=" * 60)
    
    nodes_info = {
        "interpret_question": {
            "descripción": "Interpreta preguntas en lenguaje natural sobre datos financieros",
            "entrada": "Pregunta del usuario (texto)",
            "salida": "FinancialQuestion (estructura Pydantic)",
            "funcionalidad": "Análisis semántico, clasificación de tipo de pregunta",
            "modelo": "gpt-4o-mini con structured output"
        },
        "select_data_sources": {
            "descripción": "Selecciona archivos Excel relevantes para el análisis",
            "entrada": "FinancialQuestion + archivos disponibles",
            "salida": "DataSourceSelection (estructura Pydantic)",
            "funcionalidad": "Selección inteligente de fuentes de datos",
            "modelo": "gpt-4o-mini con structured output"
        },
        "load_and_analyze": {
            "descripción": "Carga datos y realiza análisis financiero cuantitativo",
            "entrada": "DataSourceSelection + datos Excel",
            "salida": "FinancialAnalysis (estructura Pydantic)",
            "funcionalidad": "Procesamiento de datos, cálculos financieros",
            "modelo": "Pandas + NumPy + lógica de análisis"
        },
        "format_response": {
            "descripción": "Formatea resultados en respuesta ejecutiva",
            "entrada": "FinancialAnalysis + contexto",
            "salida": "Respuesta formateada (texto)",
            "funcionalidad": "Estructuración de respuesta, insights",
            "modelo": "gpt-4o-mini + templates"
        }
    }
    
    for node, info in nodes_info.items():
        print(f"\n🔵 NODO: {node}")
        print(f"   📝 Descripción: {info['descripción']}")
        print(f"   📥 Entrada: {info['entrada']}")
        print(f"   📤 Salida: {info['salida']}")
        print(f"   ⚙️  Funcionalidad: {info['funcionalidad']}")
        print(f"   🤖 Modelo: {info['modelo']}")
    
    print("\n🔄 FLUJO DE DATOS:")
    print("   Usuario → interpret_question → select_data_sources → load_and_analyze → format_response → Usuario")
    
    print("\n🎯 CARACTERÍSTICAS DEL GRAFO:")
    print("   ✅ Flujo secuencial y determinístico")
    print("   ✅ Manejo de errores en cada nodo")
    print("   ✅ Trazabilidad completa de datos")
    print("   ✅ Respuestas estructuradas y ejecutivas")
    print("   ✅ Análisis cuantitativo robusto")


def main():
    """Función principal para visualizar el grafo."""
    print("🎯 FINANCIAL AGENT - VISUALIZACIÓN DEL GRAFO LANGGRAPH")
    print("=" * 60)
    
    try:
        # Visualización en texto
        visualize_graph_text()
        
        print("\n" + "=" * 60)
        
        # Análisis detallado
        visualize_graph_detailed()
        
        print("\n" + "=" * 60)
        
        # Diagrama Mermaid
        visualize_graph_mermaid()
        
        print("\n" + "=" * 60)
        
        # Visualización gráfica (requiere matplotlib)
        try:
            visualize_graph_interactive()
        except ImportError:
            print("⚠️  Para visualización gráfica, instala: pip install matplotlib networkx")
        except Exception as e:
            print(f"⚠️  Error en visualización gráfica: {e}")
        
        print("\n✅ Visualización completada!")
        
    except Exception as e:
        print(f"❌ Error en la visualización: {e}")


if __name__ == "__main__":
    main() 