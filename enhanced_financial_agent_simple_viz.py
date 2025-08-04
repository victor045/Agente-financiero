"""
Enhanced Financial Agent - Versión Simple con Visualización.
Versión simplificada que muestra la visualización correctamente.
"""

import sys
import logging
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

try:
    import pandas as pd
    import numpy as np
    import matplotlib
    matplotlib.use('TkAgg')  # Usar backend que funciona mejor
    import matplotlib.pyplot as plt
    import networkx as nx
    import matplotlib.patches as mpatches
except ImportError as e:
    print(f"⚠️  Error de importación: {e}")
    print("💡 Instala las dependencias: pip install pandas numpy matplotlib networkx")
    sys.exit(1)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


###################
# Configuration
###################

@dataclass
class FinancialAgentConfig:
    """Configuración del agente financiero."""
    
    # Configuración de análisis
    max_analysis_iterations: int = 3
    allow_clarification: bool = True
    
    # Configuración de datos
    data_directory: str = "Datasets v2/Datasets v2"
    supported_file_types: List[str] = None
    
    # Configuración de visualización
    enable_graph_visualization: bool = True
    enable_console_progress: bool = True
    
    def __post_init__(self):
        if self.supported_file_types is None:
            self.supported_file_types = [".xlsx", ".csv", ".json"]


###################
# Simple Graph Visualization
###################

class SimpleGraphVisualizer:
    """Visualizador simple del grafo del agente financiero."""
    
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.G = self.create_graph()
        self.current_node = None
        self.completed_nodes = set()
        self.node_colors = []
        self.node_sizes = []
        
    def create_graph(self):
        """Crear el grafo del agente financiero."""
        G = nx.DiGraph()
        
        # Nodos del grafo
        nodes = [
            "interpret_question",
            "clarify_question", 
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
            ("interpret_question", "clarify_question"),
            ("interpret_question", "select_data_sources"),
            ("clarify_question", "interpret_question"),
            ("clarify_question", "END"),
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
        pos = nx.spring_layout(self.G, k=3, iterations=50, seed=42)
        
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
            'clarify_question': 'Aclarar\nPregunta',
            'select_data_sources': 'Seleccionar\nFuentes',
            'load_and_analyze': 'Cargar y\nAnalizar',
            'format_response': 'Formatear\nRespuesta',
            'END': 'FIN'
        }
        
        nx.draw_networkx_labels(self.G, pos, labels, 
                               font_size=9, font_weight='bold',
                               ax=self.ax)
        
        # Agregar título con timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        if self.current_node:
            title = f"🎯 Financial Agent - Nodo Actual: {self.current_node} [{timestamp}]"
        else:
            title = f"🎯 Financial Agent - Esperando... [{timestamp}]"
        
        self.ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
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
    
    def update_display(self):
        """Actualizar la visualización."""
        self.draw_graph()
        plt.draw()
        plt.pause(0.1)  # Pausa corta para actualizar
    
    def show_initial_graph(self):
        """Mostrar el grafo inicial."""
        self.update_display()
        plt.show(block=False)
    
    def update_progress(self, current_node, completed_nodes=None):
        """Actualizar progreso desde el agente."""
        if completed_nodes is None:
            completed_nodes = set()
        
        self.update_node_status(current_node, completed_nodes)
        self.update_display()


###################
# State Management
###################

class FinancialAgentState:
    """Estado del agente financiero."""
    
    def __init__(self):
        self.current_question: Optional[str] = None
        self.question_type: Optional[str] = None
        self.data_sources: List[str] = []
        self.analysis_results: Dict[str, Any] = {}
        self.raw_data: Dict[str, pd.DataFrame] = {}
        self.error_log: List[str] = []
        self.execution_steps: List[str] = []
        self.clarification_needed: bool = False
        self.clarification_question: str = ""


###################
# Data Processing
###################

class FinancialDataProcessor:
    """Procesador de datos financieros."""
    
    def __init__(self, config: FinancialAgentConfig):
        self.config = config
        self.data_directory = Path(config.data_directory)
        self.data = {}
    
    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        """Cargar todos los datos disponibles."""
        print("📊 Cargando datos financieros...")
        
        for file_path in self.data_directory.glob("*"):
            if file_path.suffix.lower() in self.config.supported_file_types:
                try:
                    if file_path.suffix.lower() == '.xlsx':
                        df = pd.read_excel(file_path)
                    elif file_path.suffix.lower() == '.csv':
                        df = pd.read_csv(file_path)
                    else:
                        continue
                    
                    # Limpiar datos
                    df = self._clean_dataframe(df)
                    self.data[file_path.stem] = df
                    print(f"✅ {file_path.name}: {len(df)} registros")
                    
                except Exception as e:
                    print(f"❌ Error cargando {file_path.name}: {e}")
        
        return self.data
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpiar y preprocesar dataframe."""
        # Limpiar nombres de columnas
        df.columns = df.columns.str.strip().str.replace(' ', '_')
        
        # Manejar valores faltantes
        df = df.fillna(0)
        
        # Convertir columnas numéricas
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        return df
    
    def analyze_facturas(self) -> Dict[str, Any]:
        """Análisis completo de facturas."""
        if 'facturas' not in self.data:
            return {}
        
        df = self.data['facturas']
        analysis = {}
        
        # Análisis básico
        if 'Monto_MXN' in df.columns or 'Monto_(MXN)' in df.columns:
            amount_col = 'Monto_MXN' if 'Monto_MXN' in df.columns else 'Monto_(MXN)'
            analysis['total'] = df[amount_col].sum()
            analysis['promedio'] = df[amount_col].mean()
            analysis['min'] = df[amount_col].min()
            analysis['max'] = df[amount_col].max()
            analysis['count'] = len(df)
        
        # Análisis por tipo
        if 'Tipo' in df.columns and (amount_col := self._get_amount_column(df)):
            por_cobrar = df[df['Tipo'] == 'Por cobrar'][amount_col].sum()
            por_pagar = df[df['Tipo'] == 'Por pagar'][amount_col].sum()
            analysis['por_cobrar'] = por_cobrar
            analysis['por_pagar'] = por_pagar
            
            # Análisis detallado por tipo
            facturas_por_cobrar = df[df['Tipo'] == 'Por cobrar']
            facturas_por_pagar = df[df['Tipo'] == 'Por pagar']
            
            if not facturas_por_cobrar.empty:
                analysis['por_cobrar_max'] = facturas_por_cobrar[amount_col].max()
                analysis['por_cobrar_min'] = facturas_por_cobrar[amount_col].min()
                analysis['por_cobrar_count'] = len(facturas_por_cobrar)
                analysis['por_cobrar_promedio'] = facturas_por_cobrar[amount_col].mean()
            
            if not facturas_por_pagar.empty:
                analysis['por_pagar_max'] = facturas_por_pagar[amount_col].max()
                analysis['por_pagar_min'] = facturas_por_pagar[amount_col].min()
                analysis['por_pagar_count'] = len(facturas_por_pagar)
                analysis['por_pagar_promedio'] = facturas_por_pagar[amount_col].mean()
        
        return analysis
    
    def _get_amount_column(self, df: pd.DataFrame) -> Optional[str]:
        """Obtener la columna de monto correcta."""
        amount_columns = ['Monto_MXN', 'Monto_(MXN)', 'Monto', 'Amount']
        for col in amount_columns:
            if col in df.columns:
                return col
        return None
    
    def analyze_gastos_fijos(self) -> Dict[str, Any]:
        """Análisis de gastos fijos."""
        if 'gastos_fijos' not in self.data:
            return {}
        
        df = self.data['gastos_fijos']
        analysis = {}
        
        # Análisis básico
        if 'Monto' in df.columns:
            analysis['total_gastos'] = df['Monto'].sum()
            analysis['promedio_gastos'] = df['Monto'].mean()
            analysis['count_gastos'] = len(df)
        
        # Análisis por categoría
        if 'Categoria' in df.columns and 'Monto' in df.columns:
            analysis['por_categoria'] = df.groupby('Categoria')['Monto'].sum().to_dict()
        
        return analysis
    
    def analyze_estado_cuenta(self) -> Dict[str, Any]:
        """Análisis del estado de cuenta."""
        if 'Estado_cuenta' not in self.data:
            return {}
        
        df = self.data['Estado_cuenta']
        analysis = {}
        
        # Análisis básico
        if 'Monto' in df.columns:
            analysis['total_movimientos'] = df['Monto'].sum()
            analysis['count_movimientos'] = len(df)
        
        # Análisis por tipo de movimiento
        if 'Tipo' in df.columns and 'Monto' in df.columns:
            analysis['por_tipo'] = df.groupby('Tipo')['Monto'].sum().to_dict()
        
        return analysis


###################
# Question Interpreter
###################

class QuestionInterpreter:
    """Intérprete de preguntas financieras con aclaraciones."""
    
    @staticmethod
    def interpret_question(question: str) -> Dict[str, Any]:
        """Interpretar la pregunta del usuario."""
        question_lower = question.lower()
        
        # Determinar tipo de pregunta
        if 'por pagar' in question_lower and 'alta' in question_lower:
            question_type = "facturas_por_pagar_max"
            data_sources = ["facturas.xlsx"]
            clarification_needed = False
        elif 'por cobrar' in question_lower and 'alta' in question_lower:
            question_type = "facturas_por_cobrar_max"
            data_sources = ["facturas.xlsx"]
            clarification_needed = False
        elif 'factura' in question_lower and ('alta' in question_lower or 'mayor' in question_lower or 'más alta' in question_lower):
            question_type = "facturas_max_general"
            data_sources = ["facturas.xlsx"]
            clarification_needed = False
        elif 'total' in question_lower and 'facturas' in question_lower:
            question_type = "facturas_total"
            data_sources = ["facturas.xlsx"]
            clarification_needed = False
        elif 'promedio' in question_lower and 'facturas' in question_lower:
            question_type = "facturas_promedio"
            data_sources = ["facturas.xlsx"]
            clarification_needed = False
        elif 'gastos' in question_lower:
            question_type = "gastos_analisis"
            data_sources = ["gastos_fijos.xlsx"]
            clarification_needed = False
        elif 'flujo' in question_lower or 'cuenta' in question_lower:
            question_type = "flujo_caja"
            data_sources = ["Estado_cuenta.xlsx"]
            clarification_needed = False
        elif len(question.split()) < 3:
            # Pregunta muy corta, necesita aclaración
            question_type = "general"
            data_sources = ["facturas.xlsx", "gastos_fijos.xlsx", "Estado_cuenta.xlsx"]
            clarification_needed = True
        else:
            question_type = "general"
            data_sources = ["facturas.xlsx", "gastos_fijos.xlsx", "Estado_cuenta.xlsx"]
            clarification_needed = False
        
        return {
            "question_type": question_type,
            "data_sources": data_sources,
            "analysis_required": f"Análisis de {question_type}",
            "clarification_needed": clarification_needed,
            "clarification_question": QuestionInterpreter._get_clarification_question(question, question_type)
        }
    
    @staticmethod
    def _get_clarification_question(question: str, question_type: str) -> str:
        """Generar pregunta de aclaración."""
        if question_type == "general" and len(question.split()) < 3:
            return """
🤔 Necesito más información para ayudarte mejor. 

¿Podrías especificar qué tipo de análisis financiero necesitas?

Ejemplos de preguntas que puedo responder:
- ¿Cuál es la factura por pagar más alta?
- ¿Cuál es el total de facturas emitidas?
- ¿Cuál es el promedio de facturas por cobrar?
- ¿Cuáles son los gastos fijos más altos?
- ¿Cómo está el flujo de caja?

Por favor, reformula tu pregunta con más detalles.
"""
        return ""


###################
# Response Formatter
###################

class ResponseFormatter:
    """Formateador de respuestas ejecutivas."""
    
    @staticmethod
    def format_response(question: str, analysis_results: Dict[str, Any], question_type: str) -> str:
        """Formatear respuesta basada en el tipo de pregunta."""
        
        if question_type == "facturas_por_pagar_max" and 'por_pagar_max' in analysis_results:
            return f"""
📊 Executive Summary
La factura por pagar más alta es: ${analysis_results['por_pagar_max']:,.2f} MXN

📈 Detailed Analysis
- Factura por pagar más alta: ${analysis_results['por_pagar_max']:,.2f} MXN
- Total facturas por pagar: {analysis_results.get('por_pagar_count', 0)}
- Promedio facturas por pagar: ${analysis_results.get('por_pagar_promedio', 0):,.2f} MXN
- Total por pagar: ${analysis_results.get('por_pagar', 0):,.2f} MXN

🔍 Data Sources Used
- facturas.xlsx: Tipo, Monto (MXN) - Filtrado por "Por pagar"

💡 Key Insights
- La factura por pagar más alta representa ${(analysis_results['por_pagar_max']/analysis_results.get('por_pagar', 1)*100):.1f}% del total por pagar
- Cantidad específica: ${analysis_results['por_pagar_max']:,.2f} pesos mexicanos
"""
        
        elif question_type == "facturas_por_cobrar_max" and 'por_cobrar_max' in analysis_results:
            return f"""
📊 Executive Summary
La factura por cobrar más alta es: ${analysis_results['por_cobrar_max']:,.2f} MXN

📈 Detailed Analysis
- Factura por cobrar más alta: ${analysis_results['por_cobrar_max']:,.2f} MXN
- Total facturas por cobrar: {analysis_results.get('por_cobrar_count', 0)}
- Promedio facturas por cobrar: ${analysis_results.get('por_cobrar_promedio', 0):,.2f} MXN
- Total por cobrar: ${analysis_results.get('por_cobrar', 0):,.2f} MXN

🔍 Data Sources Used
- facturas.xlsx: Tipo, Monto (MXN) - Filtrado por "Por cobrar"

💡 Key Insights
- La factura por cobrar más alta representa ${(analysis_results['por_cobrar_max']/analysis_results.get('por_cobrar', 1)*100):.1f}% del total por cobrar
- Cantidad específica: ${analysis_results['por_cobrar_max']:,.2f} pesos mexicanos
"""
        
        elif question_type == "facturas_max_general" and 'max' in analysis_results:
            return f"""
📊 Executive Summary
La factura más alta es: ${analysis_results['max']:,.2f} MXN

📈 Detailed Analysis
- Factura más alta: ${analysis_results['max']:,.2f} MXN
- Total facturas: {analysis_results.get('count', 0)}
- Promedio de facturas: ${analysis_results.get('promedio', 0):,.2f} MXN
- Factura más baja: ${analysis_results.get('min', 0):,.2f} MXN

🔍 Data Sources Used
- facturas.xlsx: Monto (MXN) - Análisis completo

💡 Key Insights
- La factura más alta representa ${(analysis_results['max']/analysis_results.get('total', 1)*100):.1f}% del total de facturas
- Cantidad específica: ${analysis_results['max']:,.2f} pesos mexicanos
"""
        
        elif question_type == "facturas_promedio" and 'promedio' in analysis_results:
            return f"""
📊 Executive Summary
Promedio de facturas: ${analysis_results['promedio']:,.2f} MXN

📈 Detailed Analysis
- Promedio por factura: ${analysis_results['promedio']:,.2f} MXN
- Total facturas: {analysis_results.get('count', 0)}
- Rango: ${analysis_results.get('min', 0):,.2f} - ${analysis_results.get('max', 0):,.2f} MXN

🔍 Data Sources Used
- facturas.xlsx: Monto (MXN)

💡 Key Insights
- El promedio de factura es ${analysis_results['promedio']:,.2f} MXN
- Cantidad específica: ${analysis_results['promedio']:,.2f} pesos mexicanos
"""
        
        elif question_type == "facturas_total":
            return f"""
📊 Executive Summary
Total de facturas emitidas: ${analysis_results['total']:,.2f} MXN

📈 Detailed Analysis
- Total facturas: ${analysis_results['total']:,.2f} MXN
- Número de facturas: {analysis_results.get('count', 0)}
- Promedio por factura: ${analysis_results.get('promedio', 0):,.2f} MXN
- Factura más alta: ${analysis_results.get('max', 0):,.2f} MXN
- Factura más baja: ${analysis_results.get('min', 0):,.2f} MXN

🔍 Data Sources Used
- facturas.xlsx: Folio de Factura, Tipo, Cliente/Proveedor, Fecha de Emisión, Monto (MXN)

💡 Key Insights
- Total de ingresos por facturas: ${analysis_results['total']:,.2f} MXN
- Promedio de factura: ${analysis_results.get('promedio', 0):,.2f} MXN
- Cantidad específica: ${analysis_results['total']:,.2f} pesos mexicanos
"""
        
        else:
            return f"""
📊 Executive Summary
Análisis general de facturas

📈 Detailed Analysis
- Total facturas: ${analysis_results.get('total', 0):,.2f} MXN
- Por cobrar: ${analysis_results.get('por_cobrar', 0):,.2f} MXN
- Por pagar: ${analysis_results.get('por_pagar', 0):,.2f} MXN
- Factura más alta: ${analysis_results.get('max', 0):,.2f} MXN
- Factura más baja: ${analysis_results.get('min', 0):,.2f} MXN
- Promedio: ${analysis_results.get('promedio', 0):,.2f} MXN

🔍 Data Sources Used
- facturas.xlsx: Datos completos de facturas

💡 Key Insights
- Análisis completado para la pregunta: "{question}"
- Cantidades específicas disponibles en el análisis detallado
- La factura más alta es: ${analysis_results.get('max', 0):,.2f} pesos mexicanos
"""


###################
# Enhanced Financial Agent Simple Viz
###################

class EnhancedFinancialAgentSimpleViz:
    """Agente financiero con visualización simple."""
    
    def __init__(self, config: FinancialAgentConfig = None):
        self.config = config or FinancialAgentConfig()
        self.data_processor = FinancialDataProcessor(self.config)
        self.question_interpreter = QuestionInterpreter()
        self.response_formatter = ResponseFormatter()
        self.visualizer = SimpleGraphVisualizer() if self.config.enable_graph_visualization else None
        self.current_state = None
        self.execution_history = []
        
        # Mostrar grafo inicial si está habilitada la visualización
        if self.visualizer and self.config.enable_graph_visualization:
            print("🎯 Iniciando visualización del grafo...")
            self.visualizer.show_initial_graph()
            time.sleep(1)
    
    def show_progress(self, step_name: str, description: str = ""):
        """Mostrar progreso del paso actual."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n🔄 [{timestamp}] PASO: {step_name}")
        if description:
            print(f"   📝 {description}")
        
        # Actualizar visualización si está habilitada
        if self.visualizer and self.config.enable_graph_visualization:
            try:
                self.visualizer.update_progress(step_name, self.current_state.execution_steps if self.current_state else set())
            except Exception as e:
                print(f"⚠️  Error actualizando visualización: {e}")
    
    def process_question(self, question: str) -> str:
        """Procesar una pregunta financiera."""
        print(f"\n🎯 PROCESANDO: {question}")
        print("=" * 60)
        
        # Inicializar estado
        state = FinancialAgentState()
        state.current_question = question
        self.current_state = state
        
        try:
            # Paso 1: Interpretar pregunta
            self.show_progress("interpret_question", "Analizando la pregunta del usuario...")
            time.sleep(1)  # Simular procesamiento
            interpretation = self.question_interpreter.interpret_question(question)
            state.question_type = interpretation["question_type"]
            state.data_sources = interpretation["data_sources"]
            state.clarification_needed = interpretation["clarification_needed"]
            state.clarification_question = interpretation["clarification_question"]
            state.execution_steps.append("interpret_question")
            print(f"   ✅ Interpretación completada: {state.question_type}")
            
            # Verificar si necesita aclaración
            if state.clarification_needed:
                self.show_progress("clarify_question", "Solicitando aclaración...")
                state.execution_steps.append("clarify_question")
                return state.clarification_question
            
            # Paso 2: Seleccionar fuentes de datos
            self.show_progress("select_data_sources", "Seleccionando archivos Excel relevantes...")
            time.sleep(1)
            print(f"   ✅ Fuentes seleccionadas: {', '.join(state.data_sources)}")
            state.execution_steps.append("select_data_sources")
            
            # Paso 3: Cargar y analizar
            self.show_progress("load_and_analyze", "Cargando datos y realizando análisis...")
            time.sleep(2)
            state.raw_data = self.data_processor.load_all_data()
            
            # Realizar análisis según el tipo de pregunta
            if 'facturas' in state.question_type:
                analysis_results = self.data_processor.analyze_facturas()
            elif 'gastos' in state.question_type:
                analysis_results = self.data_processor.analyze_gastos_fijos()
            elif 'flujo' in state.question_type or 'cuenta' in state.question_type:
                analysis_results = self.data_processor.analyze_estado_cuenta()
            else:
                # Análisis general
                analysis_results = self.data_processor.analyze_facturas()
            
            state.analysis_results = analysis_results
            state.execution_steps.append("load_and_analyze")
            print(f"   ✅ Análisis completado: {len(analysis_results)} métricas calculadas")
            
            # Paso 4: Formatear respuesta
            self.show_progress("format_response", "Formateando respuesta ejecutiva...")
            time.sleep(1)
            response = self.response_formatter.format_response(question, analysis_results, state.question_type)
            state.execution_steps.append("format_response")
            
            # Paso 5: Finalizar
            self.show_progress("END", "Proceso completado")
            time.sleep(0.5)
            state.execution_steps.append("END")
            
            return response
            
        except Exception as e:
            error_msg = f"❌ Error procesando pregunta: {e}"
            print(error_msg)
            state.error_log.append(error_msg)
            return error_msg
    
    def show_execution_summary(self):
        """Mostrar resumen de la ejecución."""
        if self.current_state:
            print("\n📊 RESUMEN DE EJECUCIÓN")
            print("=" * 60)
            print(f"Pregunta: {self.current_state.current_question}")
            print(f"Tipo de análisis: {self.current_state.question_type}")
            print(f"Fuentes utilizadas: {', '.join(self.current_state.data_sources)}")
            print(f"Archivos cargados: {list(self.current_state.raw_data.keys())}")
            print(f"Pasos ejecutados: {len(self.current_state.execution_steps)}")
            print(f"Errores: {len(self.current_state.error_log)}")
            if self.current_state.clarification_needed:
                print(f"Aclaración solicitada: Sí")


###################
# Main Function
###################

def main():
    """Función principal del agente con visualización simple."""
    print("🎯 ENHANCED FINANCIAL AGENT - CON VISUALIZACIÓN SIMPLE")
    print("=" * 60)
    print("💡 Basado en las mejores prácticas de open_deep_research")
    print("📊 Características:")
    print("   ✅ Procesamiento robusto de datos")
    print("   ✅ Análisis financiero especializado")
    print("   ✅ Respuestas estructuradas")
    print("   ✅ Manejo de errores")
    print("   ✅ Monitoreo de ejecución")
    print("   ✅ Visualización del grafo en tiempo real")
    print("   ✅ Preguntas de aclaración")
    print("=" * 60)
    
    # Crear agente
    agent = EnhancedFinancialAgentSimpleViz()
    
    # Ejemplos de preguntas
    example_questions = [
        "¿Cuál es la factura por pagar más alta?",
        "¿Cuál es el total de facturas emitidas?",
        "¿Cuál es el promedio de facturas por cobrar?",
        "¿Cuáles son los gastos fijos más altos?"
    ]
    
    print("\n📋 Ejemplos de preguntas:")
    for i, question in enumerate(example_questions, 1):
        print(f"   {i}. {question}")
    
    print("\n" + "=" * 60)
    
    # Loop interactivo
    while True:
        try:
            question = input("\n❓ Tu pregunta (o 'salir' para terminar): ").strip()
            
            if question.lower() in ['salir', 'exit', 'quit', 'q']:
                print("👋 ¡Hasta luego!")
                break
            
            if not question:
                continue
            
            # Procesar pregunta
            response = agent.process_question(question)
            
            # Mostrar respuesta
            print("\n" + "=" * 60)
            print("📋 RESPUESTA:")
            print("=" * 60)
            print(response)
            
            # Mostrar resumen de ejecución
            agent.show_execution_summary()
            
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Intenta con otra pregunta")


if __name__ == "__main__":
    main() 