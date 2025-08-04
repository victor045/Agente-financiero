"""
Visualización en Tiempo Real del Grafo LangGraph con Interfaz Gráfica.
"""

import sys
import time
import threading
from pathlib import Path
import logging
from datetime import datetime

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

try:
    import matplotlib.pyplot as plt
    import networkx as nx
    from matplotlib.animation import FuncAnimation
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyBboxPatch
    import numpy as np
except ImportError as e:
    print(f"⚠️  Error de importación: {e}")
    print("💡 Instala las dependencias: pip install matplotlib networkx")
    sys.exit(1)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LiveGraphVisualizer:
    """Visualizador en tiempo real del grafo LangGraph."""
    
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(14, 10))
        self.G = self.create_graph()
        self.current_node = None
        self.completed_nodes = set()
        self.node_colors = []
        self.node_sizes = []
        self.animation = None
        self.is_running = False
        
    def create_graph(self):
        """Crear el grafo LangGraph."""
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
    
    def update_node_status(self, current_node=None, completed_nodes=None):
        """Actualizar estado de los nodos."""
        if current_node:
            self.current_node = current_node
        if completed_nodes:
            self.completed_nodes = completed_nodes
        
        # Actualizar colores y tamaños de nodos
        self.node_colors = []
        self.node_sizes = []
        
        for node in self.G.nodes():
            if node == self.current_node:
                # Nodo actual - rojo brillante
                self.node_colors.append('#ff4444')
                self.node_sizes.append(4000)
            elif node in self.completed_nodes:
                # Nodos completados - verde
                self.node_colors.append('#44ff44')
                self.node_sizes.append(3000)
            elif node == "END":
                # Nodo final - gris
                self.node_colors.append('#cccccc')
                self.node_sizes.append(2000)
            else:
                # Nodos pendientes - azul claro
                self.node_colors.append('#aaaaaa')
                self.node_sizes.append(2500)
    
    def draw_graph(self):
        """Dibujar el grafo con el estado actual."""
        self.ax.clear()
        
        # Configurar layout
        pos = nx.spring_layout(self.G, k=4, iterations=50, seed=42)
        
        # Dibujar nodos
        nx.draw_networkx_nodes(self.G, pos, 
                              node_color=self.node_colors,
                              node_size=self.node_sizes,
                              alpha=0.8,
                              ax=self.ax)
        
        # Dibujar edges
        nx.draw_networkx_edges(self.G, pos, 
                              edge_color='gray',
                              arrows=True,
                              arrowsize=20,
                              arrowstyle='->',
                              width=2,
                              ax=self.ax)
        
        # Agregar etiquetas
        labels = {
            'interpret_question': 'Interpretar\nPregunta',
            'select_data_sources': 'Seleccionar\nFuentes',
            'load_and_analyze': 'Cargar y\nAnalizar',
            'format_response': 'Formatear\nRespuesta',
            'END': 'FIN'
        }
        
        nx.draw_networkx_labels(self.G, pos, labels, 
                               font_size=10, font_weight='bold',
                               ax=self.ax)
        
        # Agregar título con timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        if self.current_node:
            title = f"🎯 Financial Agent - Nodo Actual: {self.current_node} [{timestamp}]"
        else:
            title = f"🎯 Financial Agent - Esperando... [{timestamp}]"
        
        self.ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        
        # Agregar leyenda
        legend_elements = [
            mpatches.Patch(color='#ff4444', label='Nodo Actual'),
            mpatches.Patch(color='#44ff44', label='Completado'),
            mpatches.Patch(color='#aaaaaa', label='Pendiente'),
            mpatches.Patch(color='#cccccc', label='Final')
        ]
        self.ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 1))
        
        # Configurar layout
        self.ax.axis('off')
        plt.tight_layout()
    
    def animate(self, frame):
        """Función de animación."""
        self.draw_graph()
        return []
    
    def start_visualization(self):
        """Iniciar visualización en tiempo real."""
        self.is_running = True
        
        # Configurar animación
        self.animation = FuncAnimation(
            self.fig, self.animate, 
            interval=1000,  # Actualizar cada segundo
            blit=False,
            repeat=True
        )
        
        # Mostrar ventana
        plt.show()
    
    def update_progress(self, current_node, completed_nodes=None):
        """Actualizar progreso desde el agente."""
        if completed_nodes is None:
            completed_nodes = set()
        
        self.update_node_status(current_node, completed_nodes)
        
        # Forzar redibujado
        if self.is_running:
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()


class InteractiveFinancialAgentWithLiveVisualization:
    """Agente financiero con visualización en tiempo real."""
    
    def __init__(self):
        self.data_directory = Path("Datasets v2/Datasets v2")
        self.data = {}
        self.visualizer = LiveGraphVisualizer()
        self.completed_steps = set()
        self.load_data()
        
        # Iniciar visualización en hilo separado
        self.viz_thread = threading.Thread(target=self.visualizer.start_visualization)
        self.viz_thread.daemon = True
        self.viz_thread.start()
        
        # Esperar un momento para que se inicie la ventana
        time.sleep(2)
    
    def load_data(self):
        """Cargar todos los datos de Excel."""
        print("📊 Cargando datos financieros...")
        
        # Cargar facturas
        facturas_path = self.data_directory / "facturas.xlsx"
        if facturas_path.exists():
            self.data['facturas'] = pd.read_excel(facturas_path)
            print(f"✅ facturas.xlsx: {len(self.data['facturas'])} facturas")
        
        # Cargar gastos fijos
        gastos_path = self.data_directory / "gastos_fijos.xlsx"
        if gastos_path.exists():
            self.data['gastos_fijos'] = pd.read_excel(gastos_path)
            print(f"✅ gastos_fijos.xlsx: {len(self.data['gastos_fijos'])} gastos")
        
        # Cargar estado de cuenta
        estado_path = self.data_directory / "Estado_cuenta.xlsx"
        if estado_path.exists():
            self.data['Estado_cuenta'] = pd.read_excel(estado_path)
            print(f"✅ Estado_cuenta.xlsx: {len(self.data['Estado_cuenta'])} movimientos")
    
    def show_progress(self, step_name, description=""):
        """Mostrar progreso del paso actual."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        print(f"\n🔄 [{timestamp}] PASO: {step_name}")
        if description:
            print(f"   📝 {description}")
        
        # Actualizar visualización
        self.visualizer.update_progress(step_name, self.completed_steps)
    
    def mark_step_completed(self, step_name):
        """Marcar paso como completado."""
        self.completed_steps.add(step_name)
        self.visualizer.update_progress(None, self.completed_steps)
    
    def analyze_facturas(self):
        """Analizar datos de facturas."""
        if 'facturas' not in self.data:
            return {}
        
        df = self.data['facturas']
        analysis = {}
        
        if 'Monto (MXN)' in df.columns:
            analysis['total'] = df['Monto (MXN)'].sum()
            analysis['promedio'] = df['Monto (MXN)'].mean()
            analysis['min'] = df['Monto (MXN)'].min()
            analysis['max'] = df['Monto (MXN)'].max()
            analysis['count'] = len(df)
        
        if 'Tipo' in df.columns and 'Monto (MXN)' in df.columns:
            # Análisis por tipo
            por_cobrar = df[df['Tipo'] == 'Por cobrar']['Monto (MXN)'].sum()
            por_pagar = df[df['Tipo'] == 'Por pagar']['Monto (MXN)'].sum()
            analysis['por_cobrar'] = por_cobrar
            analysis['por_pagar'] = por_pagar
            
            # Análisis detallado por tipo
            facturas_por_cobrar = df[df['Tipo'] == 'Por cobrar']
            facturas_por_pagar = df[df['Tipo'] == 'Por pagar']
            
            if not facturas_por_cobrar.empty:
                analysis['por_cobrar_max'] = facturas_por_cobrar['Monto (MXN)'].max()
                analysis['por_cobrar_min'] = facturas_por_cobrar['Monto (MXN)'].min()
                analysis['por_cobrar_count'] = len(facturas_por_cobrar)
                analysis['por_cobrar_promedio'] = facturas_por_cobrar['Monto (MXN)'].mean()
            
            if not facturas_por_pagar.empty:
                analysis['por_pagar_max'] = facturas_por_pagar['Monto (MXN)'].max()
                analysis['por_pagar_min'] = facturas_por_pagar['Monto (MXN)'].min()
                analysis['por_pagar_count'] = len(facturas_por_pagar)
                analysis['por_pagar_promedio'] = facturas_por_pagar['Monto (MXN)'].mean()
        
        return analysis
    
    def process_question_with_live_visualization(self, question):
        """Procesar pregunta con visualización en tiempo real."""
        print(f"\n🎯 PROCESANDO PREGUNTA: {question}")
        print("=" * 60)
        
        # Paso 1: Interpretar pregunta
        self.show_progress("interpret_question", "Analizando la pregunta del usuario...")
        time.sleep(2)  # Simular procesamiento
        
        # Simular interpretación
        question_lower = question.lower()
        if 'por pagar' in question_lower and 'alta' in question_lower:
            question_type = "facturas_por_pagar_max"
        elif 'por cobrar' in question_lower and 'alta' in question_lower:
            question_type = "facturas_por_cobrar_max"
        elif 'total' in question_lower:
            question_type = "facturas_total"
        else:
            question_type = "general"
        
        self.mark_step_completed("interpret_question")
        print(f"   ✅ Interpretación completada: {question_type}")
        
        # Paso 2: Seleccionar fuentes de datos
        self.show_progress("select_data_sources", "Seleccionando archivos Excel relevantes...")
        time.sleep(2)
        
        selected_files = []
        if 'facturas' in question_lower:
            selected_files.append('facturas.xlsx')
        if 'gastos' in question_lower:
            selected_files.append('gastos_fijos.xlsx')
        if 'cuenta' in question_lower or 'flujo' in question_lower:
            selected_files.append('Estado_cuenta.xlsx')
        
        if not selected_files:
            selected_files = ['facturas.xlsx']  # Default
        
        self.mark_step_completed("select_data_sources")
        print(f"   ✅ Fuentes seleccionadas: {', '.join(selected_files)}")
        
        # Paso 3: Cargar y analizar
        self.show_progress("load_and_analyze", "Cargando datos y realizando análisis...")
        time.sleep(3)
        
        analysis = self.analyze_facturas()
        self.mark_step_completed("load_and_analyze")
        print(f"   ✅ Análisis completado: {len(analysis)} métricas calculadas")
        
        # Paso 4: Formatear respuesta
        self.show_progress("format_response", "Formateando respuesta ejecutiva...")
        time.sleep(2)
        
        response = self.format_response(question, analysis, question_type)
        self.mark_step_completed("format_response")
        
        # Paso 5: Finalizar
        self.show_progress("END", "Proceso completado")
        time.sleep(1)
        
        return response
    
    def format_response(self, question, analysis, question_type):
        """Formatear respuesta basada en el tipo de pregunta."""
        if question_type == "facturas_por_pagar_max" and 'por_pagar_max' in analysis:
            return f"""
📊 Executive Summary
La factura por pagar más alta es: ${analysis['por_pagar_max']:,.2f} MXN

📈 Detailed Analysis
- Factura por pagar más alta: ${analysis['por_pagar_max']:,.2f} MXN
- Total facturas por pagar: {analysis['por_pagar_count']}
- Promedio facturas por pagar: ${analysis['por_pagar_promedio']:,.2f} MXN
- Total por pagar: ${analysis['por_pagar']:,.2f} MXN

🔍 Data Sources Used
- facturas.xlsx: Tipo, Monto (MXN) - Filtrado por "Por pagar"

💡 Key Insights
- La factura por pagar más alta representa ${(analysis['por_pagar_max']/analysis['por_pagar']*100):.1f}% del total por pagar
- Cantidad específica: ${analysis['por_pagar_max']:,.2f} pesos mexicanos
"""
        
        elif question_type == "facturas_por_cobrar_max" and 'por_cobrar_max' in analysis:
            return f"""
📊 Executive Summary
La factura por cobrar más alta es: ${analysis['por_cobrar_max']:,.2f} MXN

📈 Detailed Analysis
- Factura por cobrar más alta: ${analysis['por_cobrar_max']:,.2f} MXN
- Total facturas por cobrar: {analysis['por_cobrar_count']}
- Promedio facturas por cobrar: ${analysis['por_cobrar_promedio']:,.2f} MXN
- Total por cobrar: ${analysis['por_cobrar']:,.2f} MXN

🔍 Data Sources Used
- facturas.xlsx: Tipo, Monto (MXN) - Filtrado por "Por cobrar"

💡 Key Insights
- La factura por cobrar más alta representa ${(analysis['por_cobrar_max']/analysis['por_cobrar']*100):.1f}% del total por cobrar
- Cantidad específica: ${analysis['por_cobrar_max']:,.2f} pesos mexicanos
"""
        
        else:
            return f"""
📊 Executive Summary
Análisis general de facturas

📈 Detailed Analysis
- Total facturas: ${analysis['total']:,.2f} MXN
- Por cobrar: ${analysis.get('por_cobrar', 0):,.2f} MXN
- Por pagar: ${analysis.get('por_pagar', 0):,.2f} MXN

🔍 Data Sources Used
- facturas.xlsx: Datos completos de facturas

💡 Key Insights
- Análisis completado para la pregunta: "{question}"
- Cantidades específicas disponibles en el análisis detallado
"""


def main():
    """Función principal del agente con visualización en tiempo real."""
    print("🎯 FINANCIAL AGENT - VISUALIZACIÓN EN TIEMPO REAL")
    print("=" * 60)
    print("💡 Haz preguntas sobre tus datos financieros")
    print("📊 Ejemplos de preguntas:")
    print("   - ¿Cuál es el total de facturas emitidas?")
    print("   - ¿Cuál es la factura por pagar más alta?")
    print("   - ¿Cuál es la factura por cobrar más alta?")
    print("=" * 60)
    
    try:
        agent = InteractiveFinancialAgentWithLiveVisualization()
        
        while True:
            try:
                question = input("\n❓ Tu pregunta (o 'salir' para terminar): ").strip()
                
                if question.lower() in ['salir', 'exit', 'quit', 'q']:
                    print("👋 ¡Hasta luego!")
                    break
                
                if not question:
                    continue
                
                # Procesar pregunta con visualización en tiempo real
                response = agent.process_question_with_live_visualization(question)
                
                # Mostrar respuesta
                print("\n" + "=" * 60)
                print("📋 RESPUESTA:")
                print("=" * 60)
                print(response)
                
            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("💡 Intenta con otra pregunta")
                
    except Exception as e:
        print(f"❌ Error inicializando visualización: {e}")


if __name__ == "__main__":
    main() 