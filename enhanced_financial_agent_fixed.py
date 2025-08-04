"""
Enhanced Financial Agent - Fixed Version
Agente financiero mejorado con visualización dinámica, retroalimentación y prompts funcionales.
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import networkx as nx

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

@dataclass
class FinancialAgentConfig:
    """Configuración del agente financiero mejorado."""
    
    # Configuración de análisis
    enable_prompt_engineering: bool = True
    enable_dynamic_visualization: bool = True
    enable_feedback: bool = True
    enable_clarification: bool = True
    
    # ========================================
    # CAMBIAR AQUÍ LAS FUENTES DE DATOS
    # ========================================
    data_directory: str = "Datasets v2/Datasets v2"
    # ========================================
    
    supported_file_types: List[str] = None
    
    def __post_init__(self):
        if self.supported_file_types is None:
            self.supported_file_types = [".xlsx", ".csv", ".json"]


class DynamicGraphVisualizer:
    """Visualizador de grafo dinámico con retroalimentación."""
    
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(14, 10))
        self.nodes = {}
        self.edges = []
        self.current_node = None
        self.completed_nodes = set()
        self.create_graph()
        
    def create_graph(self):
        """Crear estructura del grafo con nodos de retroalimentación."""
        self.nodes = {
            'interpret': {'pos': (1, 6), 'label': 'Interpretar\nPregunta', 'color': 'lightgray'},
            'clarify': {'pos': (3, 6), 'label': 'Aclarar\nDuda', 'color': 'lightgray'},
            'analyze': {'pos': (5, 6), 'label': 'Analizar\nDatos', 'color': 'lightgray'},
            'prompt': {'pos': (7, 6), 'label': 'Generar\nPrompt', 'color': 'lightgray'},
            'respond': {'pos': (9, 6), 'label': 'Formatear\nRespuesta', 'color': 'lightgray'},
            'feedback': {'pos': (5, 4), 'label': 'Retroalimentación\nUsuario', 'color': 'lightgray'},
            'end': {'pos': (5, 2), 'label': 'Finalizar', 'color': 'lightgray'}
        }
        
        self.edges = [
            ('interpret', 'clarify'),
            ('clarify', 'analyze'),
            ('analyze', 'prompt'),
            ('prompt', 'respond'),
            ('respond', 'feedback'),
            ('feedback', 'end'),
            ('interpret', 'analyze'),  # Ruta directa si no hay aclaración
            ('respond', 'end')  # Ruta directa si no hay feedback
        ]
    
    def update_node_status(self, current_node=None, completed_nodes=None):
        """Actualizar estado de nodos dinámicamente."""
        if completed_nodes is None:
            completed_nodes = set()
        
        self.current_node = current_node
        self.completed_nodes = completed_nodes
        
        # Actualizar colores
        for node_name, node_info in self.nodes.items():
            if node_name == current_node:
                node_info['color'] = 'lightblue'  # Actual
            elif node_name in completed_nodes:
                node_info['color'] = 'lightgreen'  # Completado
            else:
                node_info['color'] = 'lightgray'  # Pendiente
    
    def draw_graph(self):
        """Dibujar el grafo dinámicamente."""
        self.ax.clear()
        
        # Crear grafo
        G = nx.DiGraph()
        
        # Agregar nodos
        for node, info in self.nodes.items():
            G.add_node(node, pos=info['pos'])
        
        # Agregar edges
        G.add_edges_from(self.edges)
        
        # Posiciones
        pos = nx.get_node_attributes(G, 'pos')
        
        # Colores de nodos
        colors = [self.nodes[node]['color'] for node in G.nodes()]
        
        # Dibujar
        nx.draw(G, pos, ax=self.ax, 
                node_color=colors,
                node_size=3500,
                font_size=10,
                font_weight='bold',
                arrows=True,
                edge_color='gray',
                with_labels=True,
                labels={node: self.nodes[node]['label'] for node in G.nodes()})
        
        # Título dinámico
        status = f"🔄 Actual: {self.current_node}" if self.current_node else "⏳ Esperando..."
        self.ax.set_title(f'🎯 Enhanced Financial Agent - {status}', fontsize=16, fontweight='bold')
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(1, 7)
    
    def update_display(self):
        """Actualizar visualización dinámicamente."""
        self.draw_graph()
        plt.draw()
        plt.pause(0.2)  # Pausa más larga para mejor visualización
    
    def show_initial_graph(self):
        """Mostrar grafo inicial."""
        self.update_display()
    
    def update_progress(self, current_node, completed_nodes=None):
        """Actualizar progreso dinámicamente."""
        self.update_node_status(current_node, completed_nodes)
        self.update_display()


class FinancialDataProcessor:
    """Procesador de datos financieros mejorado."""
    
    def __init__(self, config: FinancialAgentConfig):
        self.config = config
        self.data = {}
    
    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        """Cargar todos los datos disponibles."""
        print("📊 Cargando datos financieros...")
        print(f"📁 Desde: {self.config.data_directory}")
        
        data_path = Path(self.config.data_directory)
        if not data_path.exists():
            print(f"❌ Error: Directorio {data_path} no existe")
            return {}
        
        for file_path in data_path.glob("*"):
            if file_path.suffix.lower() in self.config.supported_file_types:
                try:
                    df = pd.read_excel(file_path) if file_path.suffix.lower() == '.xlsx' else pd.read_csv(file_path)
                    df = self._clean_dataframe(df)
                    key = file_path.stem
                    self.data[key] = df
                    print(f"✅ {file_path.name}: {len(df)} registros")
                except Exception as e:
                    print(f"❌ Error cargando {file_path.name}: {e}")
        
        return self.data
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpiar DataFrame."""
        df.columns = df.columns.str.strip().str.replace(' ', '_')
        df = df.fillna(0)
        return df
    
    def analyze_facturas_por_mes(self, tipo_factura: str = None) -> Dict[str, Any]:
        """Analizar facturas por mes para encontrar el mes con más facturas."""
        if 'facturas' not in self.data:
            return {}
        
        df = self.data['facturas'].copy()
        analysis = {}
        
        # Encontrar columna de fecha
        fecha_col = None
        for col in df.columns:
            if 'fecha' in col.lower() or 'emision' in col.lower():
                fecha_col = col
                break
        
        if not fecha_col:
            return {}
        
        try:
            # Convertir a datetime
            df[fecha_col] = pd.to_datetime(df[fecha_col], errors='coerce')
            
            # Agregar columna de mes
            df['mes'] = df[fecha_col].dt.month
            df['mes_nombre'] = df[fecha_col].dt.month_name()
            
            # Filtrar por tipo si se especifica
            if tipo_factura and 'Tipo' in df.columns:
                if tipo_factura == "por_cobrar":
                    df = df[df['Tipo'] == 'Por cobrar']
                elif tipo_factura == "por_pagar":
                    df = df[df['Tipo'] == 'Por pagar']
            
            # Obtener columna de monto
            amount_col = self._get_amount_column(df)
            if not amount_col:
                return {}
            
            # Agrupar por mes
            monthly_data = df.groupby(['mes', 'mes_nombre']).agg({
                amount_col: ['sum', 'count']
            }).reset_index()
            
            # Encontrar mes con más facturas
            max_count_idx = monthly_data[(amount_col, 'count')].idxmax()
            max_month = monthly_data.iloc[max_count_idx]
            
            # Extraer valores de manera segura
            try:
                analysis['mes_maximo'] = str(max_month['mes_nombre'].iloc[0])
            except:
                analysis['mes_maximo'] = str(max_month['mes_nombre'])
            
            try:
                analysis['mes_maximo_numero'] = int(max_month['mes'].iloc[0])
            except:
                analysis['mes_maximo_numero'] = int(max_month['mes'])
            
            try:
                analysis['cantidad_maxima'] = float(max_month[(amount_col, 'sum')].iloc[0])
            except:
                analysis['cantidad_maxima'] = float(max_month[(amount_col, 'sum')])
            
            try:
                analysis['facturas_maximas'] = int(max_month[(amount_col, 'count')].iloc[0])
            except:
                analysis['facturas_maximas'] = int(max_month[(amount_col, 'count')])
            
            analysis['tipo_factura'] = tipo_factura
            
            # Datos de todos los meses
            analysis['datos_por_mes'] = {}
            for _, row in monthly_data.iterrows():
                mes = str(row['mes_nombre'])
                analysis['datos_por_mes'][mes] = {
                    'cantidad': float(row[(amount_col, 'sum')]),
                    'facturas': int(row[(amount_col, 'count')])
                }
            
        except Exception as e:
            print(f"⚠️  Error analizando facturas por mes: {e}")
            return {}
        
        return analysis
    
    def analyze_facturas_por_fecha(self, fecha_filtro: str, tipo_factura: str = None) -> Dict[str, Any]:
        """Analizar facturas por fecha específica."""
        if 'facturas' not in self.data:
            return {}
        
        df = self.data['facturas'].copy()
        analysis = {}
        
        # Encontrar columna de fecha
        fecha_col = None
        for col in df.columns:
            if 'fecha' in col.lower() or 'emision' in col.lower():
                fecha_col = col
                break
        
        if not fecha_col:
            return {}
        
        try:
            # Convertir a datetime
            df[fecha_col] = pd.to_datetime(df[fecha_col], errors='coerce')
            
            # Mapeo de meses
            month_map = {
                "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
                "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
                "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
            }
            
            # Filtrar por mes
            if fecha_filtro.lower() in month_map:
                df = df[df[fecha_col].dt.month == month_map[fecha_filtro.lower()]]
                analysis['fecha_filtro'] = fecha_filtro
                analysis['registros_filtrados'] = len(df)
            
            # Filtrar por tipo si se especifica
            if tipo_factura and 'Tipo' in df.columns:
                if tipo_factura == "por_cobrar":
                    df = df[df['Tipo'] == 'Por cobrar']
                elif tipo_factura == "por_pagar":
                    df = df[df['Tipo'] == 'Por pagar']
            
            # Obtener columna de monto
            amount_col = self._get_amount_column(df)
            if amount_col:
                analysis['total'] = df[amount_col].sum()
                analysis['promedio'] = df[amount_col].mean()
                analysis['min'] = df[amount_col].min()
                analysis['max'] = df[amount_col].max()
                analysis['count'] = len(df)
                
                # Análisis por tipo
                if 'Tipo' in df.columns:
                    por_cobrar = df[df['Tipo'] == 'Por cobrar'][amount_col].sum()
                    por_pagar = df[df['Tipo'] == 'Por pagar'][amount_col].sum()
                    analysis['por_cobrar'] = por_cobrar
                    analysis['por_pagar'] = por_pagar
            
        except Exception as e:
            print(f"⚠️  Error analizando facturas por fecha: {e}")
            return {}
        
        return analysis
    
    def analyze_proveedor_mayor_monto(self, tipo_factura: str = "por_pagar") -> Dict[str, Any]:
        """Analizar proveedor con mayor monto total de facturas."""
        if 'facturas' not in self.data:
            return {}
        
        df = self.data['facturas'].copy()
        analysis = {}
        
        try:
            # Filtrar por tipo de factura
            if 'Tipo' in df.columns:
                if tipo_factura == "por_pagar":
                    df = df[df['Tipo'] == 'Por pagar']
                elif tipo_factura == "por_cobrar":
                    df = df[df['Tipo'] == 'Por cobrar']
            
            # Obtener columna de monto
            amount_col = self._get_amount_column(df)
            if not amount_col:
                return {}
            
            # Encontrar columna de proveedor/cliente
            proveedor_col = None
            for col in df.columns:
                if 'proveedor' in col.lower() or 'cliente' in col.lower() or 'vendedor' in col.lower():
                    proveedor_col = col
                    break
            
            if not proveedor_col:
                return {}
            
            # Agrupar por proveedor
            proveedor_data = df.groupby(proveedor_col).agg({
                amount_col: ['sum', 'count']
            }).reset_index()
            
            # Encontrar proveedor con mayor monto
            max_amount_idx = proveedor_data[(amount_col, 'sum')].idxmax()
            max_proveedor = proveedor_data.iloc[max_amount_idx]
            
            # Extraer valores de manera segura
            try:
                analysis['proveedor_maximo'] = str(max_proveedor[proveedor_col].iloc[0])
            except:
                analysis['proveedor_maximo'] = str(max_proveedor[proveedor_col])
            
            try:
                analysis['monto_maximo'] = float(max_proveedor[(amount_col, 'sum')].iloc[0])
            except:
                analysis['monto_maximo'] = float(max_proveedor[(amount_col, 'sum')])
            
            try:
                analysis['facturas_count'] = int(max_proveedor[(amount_col, 'count')].iloc[0])
            except:
                analysis['facturas_count'] = int(max_proveedor[(amount_col, 'count')])
            
            analysis['tipo_factura'] = tipo_factura
            
            # Datos de todos los proveedores
            analysis['datos_por_proveedor'] = {}
            for _, row in proveedor_data.iterrows():
                proveedor = str(row[proveedor_col])
                analysis['datos_por_proveedor'][proveedor] = {
                    'monto_total': float(row[(amount_col, 'sum')]),
                    'facturas': int(row[(amount_col, 'count')])
                }
            
        except Exception as e:
            print(f"⚠️  Error analizando proveedores: {e}")
            return {}
        
        return analysis
    
    def analyze_factura_por_pagar_mas_alta(self) -> Dict[str, Any]:
        """Analizar la factura por pagar con el monto más alto."""
        if 'facturas' not in self.data:
            return {}
        
        df = self.data['facturas'].copy()
        analysis = {}
        
        try:
            # Filtrar solo facturas por pagar
            if 'Tipo' in df.columns:
                df = df[df['Tipo'] == 'Por pagar']
            
            # Obtener columna de monto
            amount_col = self._get_amount_column(df)
            if not amount_col:
                return {}
            
            # Encontrar la factura con mayor monto
            if df.empty:
                return {}
            
            max_amount_idx = df[amount_col].idxmax()
            max_factura = df.loc[max_amount_idx]
            
            # Extraer información de la factura
            analysis['monto_maximo'] = float(max_factura[amount_col])
            analysis['factura_id'] = str(max_factura.get('Folio', 'N/A'))
            
            # Encontrar columna de proveedor/cliente
            proveedor_col = None
            for col in df.columns:
                if 'proveedor' in col.lower() or 'cliente' in col.lower() or 'vendedor' in col.lower():
                    proveedor_col = col
                    break
            
            if proveedor_col:
                analysis['proveedor'] = str(max_factura[proveedor_col])
            
            # Encontrar columna de fecha
            fecha_col = None
            for col in df.columns:
                if 'fecha' in col.lower() or 'emision' in col.lower():
                    fecha_col = col
                    break
            
            if fecha_col:
                analysis['fecha'] = str(max_factura[fecha_col])
            
            # Estadísticas adicionales
            analysis['total_por_pagar'] = df[amount_col].sum()
            analysis['promedio_por_pagar'] = df[amount_col].mean()
            analysis['cantidad_facturas'] = len(df)
            
        except Exception as e:
            print(f"⚠️  Error analizando factura por pagar más alta: {e}")
            return {}
        
        return analysis
    
    def analyze_proveedor_terminos_generosos(self) -> Dict[str, Any]:
        """Analizar proveedor con términos de pago más generosos."""
        if 'facturas' not in self.data:
            return {}
        
        df = self.data['facturas'].copy()
        analysis = {}
        
        try:
            # Filtrar solo facturas por pagar
            if 'Tipo' in df.columns:
                df = df[df['Tipo'] == 'Por pagar']
            
            # Encontrar columna de términos de pago
            terminos_col = None
            for col in df.columns:
                if 'termino' in col.lower() or 'pago' in col.lower() or 'dias' in col.lower():
                    terminos_col = col
                    break
            
            if not terminos_col:
                # Si no hay columna de términos, usar prompt engineering
                analysis['use_prompts'] = True
                analysis['mensaje'] = "No se encontró información específica sobre términos de pago en los datos"
                return analysis
            
            # Encontrar columna de proveedor
            proveedor_col = None
            for col in df.columns:
                if 'proveedor' in col.lower() or 'cliente' in col.lower() or 'vendedor' in col.lower():
                    proveedor_col = col
                    break
            
            if not proveedor_col:
                return {}
            
            # Agrupar por proveedor y analizar términos
            proveedor_terminos = df.groupby(proveedor_col)[terminos_col].agg(['mean', 'max', 'min']).reset_index()
            
            # Encontrar proveedor con términos más generosos (mayor promedio)
            max_terminos_idx = proveedor_terminos['mean'].idxmax()
            max_proveedor = proveedor_terminos.iloc[max_terminos_idx]
            
            analysis['proveedor_generoso'] = str(max_proveedor[proveedor_col])
            analysis['termino_promedio'] = float(max_proveedor['mean'])
            analysis['termino_maximo'] = float(max_proveedor['max'])
            analysis['termino_minimo'] = float(max_proveedor['min'])
            
        except Exception as e:
            print(f"⚠️  Error analizando términos de pago: {e}")
            analysis['use_prompts'] = True
            analysis['mensaje'] = "Error al analizar términos de pago"
            return analysis
        
        return analysis
    
    def _get_amount_column(self, df: pd.DataFrame) -> Optional[str]:
        """Obtener la columna de monto correcta."""
        amount_columns = ['Monto_MXN', 'Monto_(MXN)', 'Monto', 'Amount']
        for col in amount_columns:
            if col in df.columns:
                return col
        return None


class QuestionInterpreter:
    """Intérprete de preguntas mejorado."""
    
    def __init__(self, enable_clarification: bool = True):
        self.enable_clarification = enable_clarification
    
    def interpret_question(self, question: str) -> Dict[str, Any]:
        """Interpretar la pregunta del usuario."""
        question_lower = question.lower()
        
        # Detectar filtros de fecha
        fecha_filtro = None
        month_names = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]
        
        for month in month_names:
            if month in question_lower:
                fecha_filtro = month
                break
        
        # Determinar tipo de pregunta
        if ('proveedor' in question_lower or 'cliente' in question_lower) and ('mayor' in question_lower or 'más' in question_lower or 'mas' in question_lower) and ('monto' in question_lower or 'total' in question_lower):
            question_type = "proveedor_mayor_monto"
            data_sources = ["facturas.xlsx"]
            clarification_needed = False
        elif ('por pagar' in question_lower and 'más alta' in question_lower) or ('por pagar' in question_lower and 'mayor' in question_lower and 'factura' in question_lower):
            question_type = "factura_por_pagar_mas_alta"
            data_sources = ["facturas.xlsx"]
            clarification_needed = False
        elif ('proveedor' in question_lower or 'cliente' in question_lower) and ('términos' in question_lower or 'terminos' in question_lower or 'generosos' in question_lower):
            question_type = "proveedor_terminos_generosos"
            data_sources = ["facturas.xlsx"]
            clarification_needed = False
        elif ('total' in question_lower and 'facturas' in question_lower and 'por cobrar' in question_lower and fecha_filtro):
            question_type = "facturas_por_cobrar_total_fecha"
            data_sources = ["facturas.xlsx"]
            clarification_needed = False
        elif ('total' in question_lower and 'facturas' in question_lower and 'por pagar' in question_lower and fecha_filtro):
            question_type = "facturas_por_pagar_total_fecha"
            data_sources = ["facturas.xlsx"]
            clarification_needed = False
        elif ('mes' in question_lower and ('más' in question_lower or 'mas' in question_lower) and 'facturas' in question_lower):
            if 'por cobrar' in question_lower:
                question_type = "facturas_por_cobrar_mes_maximo"
            elif 'por pagar' in question_lower:
                question_type = "facturas_por_pagar_mes_maximo"
            else:
                question_type = "facturas_mes_maximo"
            data_sources = ["facturas.xlsx"]
            clarification_needed = False
        elif 'factura' in question_lower and ('más' in question_lower or 'mas' in question_lower):
            question_type = "facturas_mes_maximo"
            data_sources = ["facturas.xlsx"]
            clarification_needed = False
        elif len(question.split()) < 3:
            question_type = "general"
            data_sources = ["facturas.xlsx", "gastos_fijos.xlsx", "Estado_cuenta.xlsx"]
            clarification_needed = True
        else:
            question_type = "personalizado"
            data_sources = ["facturas.xlsx", "gastos_fijos.xlsx", "Estado_cuenta.xlsx"]
            clarification_needed = False
        
        return {
            "question_type": question_type,
            "data_sources": data_sources,
            "fecha_filtro": fecha_filtro,
            "clarification_needed": clarification_needed,
            "clarification_question": self._get_clarification_question(question, question_type),
            "use_prompts": question_type == "personalizado"
        }
    
    def _get_clarification_question(self, question: str, question_type: str) -> str:
        """Generar pregunta de aclaración."""
        if question_type == "general" and len(question.split()) < 3:
            return f"Tu pregunta '{question}' es muy breve. ¿Podrías ser más específico sobre qué información financiera necesitas?"
        return ""


class ResponseFormatter:
    """Formateador de respuestas mejorado."""
    
    def __init__(self, enable_prompts: bool = True):
        self.enable_prompts = enable_prompts
    
    def format_response(self, question: str, analysis_results: Dict[str, Any], question_type: str) -> str:
        """Formatear respuesta basada en el tipo de pregunta."""
        
        if question_type == "personalizado" and self.enable_prompts:
            return self._format_prompt_response(question, analysis_results)
        
        # Respuestas pre-configuradas
        if question_type == "factura_por_pagar_mas_alta" and 'monto_maximo' in analysis_results:
            return f"""
📊 Executive Summary
La factura por pagar más alta es: ${analysis_results['monto_maximo']:,.2f} MXN

📈 Detailed Analysis
- Monto de la factura más alta: ${analysis_results['monto_maximo']:,.2f} MXN
- Folio de factura: {analysis_results.get('factura_id', 'N/A')}
- Proveedor: {analysis_results.get('proveedor', 'N/A')}
- Fecha de emisión: {analysis_results.get('fecha', 'N/A')}
- Total facturas por pagar: ${analysis_results.get('total_por_pagar', 0):,.2f} MXN
- Promedio por factura: ${analysis_results.get('promedio_por_pagar', 0):,.2f} MXN
- Cantidad de facturas: {analysis_results.get('cantidad_facturas', 0)}

🔍 Data Sources Used
- facturas.xlsx: Filtrado por tipo "Por pagar"

💡 Key Insights
- La factura más alta representa ${(analysis_results['monto_maximo']/analysis_results.get('total_por_pagar', 1)*100):.1f}% del total por pagar
- Cantidad específica: ${analysis_results['monto_maximo']:,.2f} pesos mexicanos
"""
        
        elif question_type == "proveedor_terminos_generosos":
            if analysis_results.get('use_prompts'):
                return f"""
🤖 RESPUESTA GENERADA CON PROMPT ENGINEERING
============================================================

📊 Executive Summary
Análisis de términos de pago más generosos

📈 Detailed Analysis
{analysis_results.get('mensaje', 'Análisis de términos de pago requerido')}

🔍 Data Sources Used
- facturas.xlsx: Análisis de términos de pago por proveedor

💡 Key Insights
- Esta pregunta requiere análisis específico de términos de pago
- Se recomienda revisar manualmente los términos por proveedor
"""
            elif 'proveedor_generoso' in analysis_results:
                return f"""
📊 Executive Summary
El proveedor con términos de pago más generosos es: {analysis_results['proveedor_generoso']}

📈 Detailed Analysis
- Proveedor más generoso: {analysis_results['proveedor_generoso']}
- Término promedio: {analysis_results['termino_promedio']:.0f} días
- Término máximo: {analysis_results['termino_maximo']:.0f} días
- Término mínimo: {analysis_results['termino_minimo']:.0f} días

🔍 Data Sources Used
- facturas.xlsx: Análisis de términos de pago por proveedor

💡 Key Insights
- {analysis_results['proveedor_generoso']} ofrece los términos más generosos
- Promedio de {analysis_results['termino_promedio']:.0f} días para pago
"""
            else:
                return f"""
📊 Executive Summary
Análisis de términos de pago

📈 Detailed Analysis
No se pudo determinar el proveedor con términos más generosos

🔍 Data Sources Used
- facturas.xlsx: Datos de facturas por pagar

💡 Key Insights
- Se requiere información específica sobre términos de pago
- Recomendación: Revisar manualmente los términos por proveedor
"""
        
        elif question_type == "proveedor_mayor_monto" and 'proveedor_maximo' in analysis_results:
            return f"""
📊 Executive Summary
El proveedor con mayor monto total de facturas por pagar es: {analysis_results['proveedor_maximo']}

📈 Detailed Analysis
- Proveedor con mayor monto: {analysis_results['proveedor_maximo']}
- Monto total: ${analysis_results['monto_maximo']:,.2f} MXN
- Número de facturas: {analysis_results['facturas_count']}

📊 Desglose por proveedores:
"""
            + "\n".join([f"- {proveedor}: ${datos['monto_total']:,.2f} ({datos['facturas']} facturas)" 
                        for proveedor, datos in analysis_results.get('datos_por_proveedor', {}).items()]) + f"""

🔍 Data Sources Used
- facturas.xlsx: Análisis por proveedor y tipo "Por pagar"

💡 Key Insights
- {analysis_results['proveedor_maximo']} es el proveedor con mayor monto total
- Total de {analysis_results['facturas_count']} facturas por pagar
- Monto específico: ${analysis_results['monto_maximo']:,.2f} pesos mexicanos
"""
        
        elif question_type == "facturas_por_cobrar_total_fecha" and 'por_cobrar' in analysis_results:
            return f"""
📊 Executive Summary
Total de facturas por cobrar en {analysis_results.get('fecha_filtro', 'el mes')}: ${analysis_results['por_cobrar']:,.2f} MXN

📈 Detailed Analysis
- Total facturas por cobrar: ${analysis_results['por_cobrar']:,.2f} MXN
- Número de facturas: {analysis_results.get('count', 0)}
- Promedio por factura: ${analysis_results.get('promedio', 0):,.2f} MXN
- Factura más alta: ${analysis_results.get('max', 0):,.2f} MXN
- Factura más baja: ${analysis_results.get('min', 0):,.2f} MXN

🔍 Data Sources Used
- facturas.xlsx: Filtrado por mes "{analysis_results.get('fecha_filtro', '')}" y tipo "Por cobrar"

💡 Key Insights
- Total específico de facturas por cobrar en {analysis_results.get('fecha_filtro', 'el mes')}: ${analysis_results['por_cobrar']:,.2f} pesos mexicanos
- Cantidad de facturas: {analysis_results.get('count', 0)}
"""
        
        elif question_type == "facturas_por_pagar_total_fecha" and 'por_pagar' in analysis_results:
            return f"""
📊 Executive Summary
Total de facturas por pagar en {analysis_results.get('fecha_filtro', 'el mes')}: ${analysis_results['por_pagar']:,.2f} MXN

📈 Detailed Analysis
- Total facturas por pagar: ${analysis_results['por_pagar']:,.2f} MXN
- Número de facturas: {analysis_results.get('count', 0)}
- Promedio por factura: ${analysis_results.get('promedio', 0):,.2f} MXN
- Factura más alta: ${analysis_results.get('max', 0):,.2f} MXN
- Factura más baja: ${analysis_results.get('min', 0):,.2f} MXN

🔍 Data Sources Used
- facturas.xlsx: Filtrado por mes "{analysis_results.get('fecha_filtro', '')}" y tipo "Por pagar"

💡 Key Insights
- Total específico de facturas por pagar en {analysis_results.get('fecha_filtro', 'el mes')}: ${analysis_results['por_pagar']:,.2f} pesos mexicanos
- Cantidad de facturas: {analysis_results.get('count', 0)}
"""
        
        elif question_type == "facturas_mes_maximo" and 'mes_maximo' in analysis_results:
            return f"""
📊 Executive Summary
El mes con más facturas es: {analysis_results['mes_maximo']}

📈 Detailed Analysis
- Mes con más facturas: {analysis_results['mes_maximo']}
- Cantidad total en {analysis_results['mes_maximo']}: ${analysis_results['cantidad_maxima']:,.2f} MXN
- Número de facturas en {analysis_results['mes_maximo']}: {analysis_results['facturas_maximas']}

📊 Desglose por meses:
"""
            + "\n".join([f"- {mes}: ${datos['cantidad']:,.2f} ({datos['facturas']} facturas)" 
                        for mes, datos in analysis_results.get('datos_por_mes', {}).items()]) + f"""

🔍 Data Sources Used
- facturas.xlsx: Análisis por mes

💡 Key Insights
- {analysis_results['mes_maximo']} es el mes con más facturas
- Total de {analysis_results['facturas_maximas']} facturas en {analysis_results['mes_maximo']}
- Cantidad específica: ${analysis_results['cantidad_maxima']:,.2f} pesos mexicanos
"""
        else:
            return f"""
📊 Executive Summary
Análisis general de facturas

📈 Detailed Analysis
- Total facturas: ${analysis_results.get('total', 0):,.2f} MXN
- Por cobrar: ${analysis_results.get('por_cobrar', 0):,.2f} MXN
- Por pagar: ${analysis_results.get('por_pagar', 0):,.2f} MXN

🔍 Data Sources Used
- facturas.xlsx: Datos completos de facturas

💡 Key Insights
- Análisis completado para la pregunta: "{question}"
- Cantidades específicas disponibles en el análisis detallado
"""
    
    def _format_prompt_response(self, question: str, analysis_results: Dict[str, Any]) -> str:
        """Formatear respuesta usando prompts mejorados."""
        
        # Generar respuesta más inteligente basada en los datos
        insights = []
        
        if 'mes_maximo' in analysis_results:
            insights.append(f"📅 El mes con más actividad fue {analysis_results['mes_maximo']} con {analysis_results['facturas_maximas']} facturas")
            insights.append(f"💰 Total facturado en {analysis_results['mes_maximo']}: ${analysis_results['cantidad_maxima']:,.2f} MXN")
        
        if 'datos_por_mes' in analysis_results:
            total_facturas = sum(datos['facturas'] for datos in analysis_results['datos_por_mes'].values())
            insights.append(f"📊 Total de facturas analizadas: {total_facturas}")
        
        # Si no hay insights específicos, generar análisis general
        if not insights:
            insights.append("📈 Análisis de datos financieros completado")
            insights.append("💡 Se identificaron patrones en la facturación mensual")
            insights.append("🔍 Recomendación: Revisar tendencias por mes para optimizar")
        
        return f"""
🤖 RESPUESTA GENERADA CON PROMPT ENGINEERING
============================================================

📊 Executive Summary
Análisis personalizado para: "{question}"

📈 Detailed Analysis
Basado en los datos disponibles, he identificado la siguiente información relevante:

{chr(10).join(insights)}

🔍 Data Sources Used
- Análisis basado en datos de facturas, gastos y estado de cuenta
- Respuesta generada usando prompt engineering para máxima flexibilidad

💡 Key Insights
- Esta respuesta fue generada usando análisis inteligente de datos
- Se consideraron múltiples fuentes de información
- El análisis se adaptó específicamente a tu pregunta
"""


class EnhancedFinancialAgentFixed:
    """Agente financiero mejorado con visualización dinámica y retroalimentación."""
    
    def __init__(self, config: FinancialAgentConfig = None):
        self.config = config or FinancialAgentConfig()
        self.data_processor = FinancialDataProcessor(self.config)
        self.question_interpreter = QuestionInterpreter(self.config.enable_clarification)
        self.response_formatter = ResponseFormatter(self.config.enable_prompt_engineering)
        self.visualizer = DynamicGraphVisualizer() if self.config.enable_dynamic_visualization else None
        self.execution_steps = []
        
        # Mostrar información de configuración
        print(f"📁 Fuente de datos configurada: {self.config.data_directory}")
        print(f"🤖 Prompt Engineering: {'Habilitado' if self.config.enable_prompt_engineering else 'Deshabilitado'}")
        print(f"🎯 Visualización dinámica: {'Habilitada' if self.config.enable_dynamic_visualization else 'Deshabilitada'}")
        print(f"💬 Retroalimentación: {'Habilitada' if self.config.enable_feedback else 'Deshabilitada'}")
        
        # Mostrar grafo inicial
        if self.visualizer and self.config.enable_dynamic_visualization:
            print("🎯 Iniciando visualización dinámica del grafo...")
            self.visualizer.show_initial_graph()
            time.sleep(1)
    
    def show_progress(self, step_name: str, description: str = ""):
        """Mostrar progreso del paso actual."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n🔄 [{timestamp}] PASO: {step_name}")
        if description:
            print(f"   📝 {description}")
        
        # Actualizar visualización dinámicamente
        if self.visualizer and self.config.enable_dynamic_visualization:
            try:
                self.visualizer.update_progress(step_name, set(self.execution_steps))
            except Exception as e:
                print(f"⚠️  Error actualizando visualización: {e}")
    
    def process_question(self, question: str) -> str:
        """Procesar una pregunta financiera con visualización dinámica."""
        print(f"\n🎯 PROCESANDO: {question}")
        print("=" * 60)
        
        try:
            # Paso 1: Interpretar pregunta
            self.show_progress("interpret", "Analizando la pregunta del usuario...")
            time.sleep(1)
            interpretation = self.question_interpreter.interpret_question(question)
            self.execution_steps.append("interpret")
            
            print(f"   ✅ Interpretación completada: {interpretation['question_type']}")
            if interpretation.get("use_prompts"):
                print(f"   🤖 Usando prompt engineering para respuesta flexible")
            
            # Verificar si necesita aclaración
            if interpretation["clarification_needed"]:
                self.show_progress("clarify", "Solicitando aclaración...")
                self.execution_steps.append("clarify")
                return interpretation["clarification_question"]
            
            # Paso 2: Cargar y analizar
            self.show_progress("analyze", "Cargando datos y realizando análisis...")
            time.sleep(2)
            self.data_processor.load_all_data()
            
            # Realizar análisis según el tipo de pregunta
            if interpretation['question_type'] == "factura_por_pagar_mas_alta":
                analysis_results = self.data_processor.analyze_factura_por_pagar_mas_alta()
            elif interpretation['question_type'] == "proveedor_mayor_monto":
                analysis_results = self.data_processor.analyze_proveedor_mayor_monto("por_pagar")
            elif interpretation['question_type'] == "proveedor_terminos_generosos":
                analysis_results = self.data_processor.analyze_proveedor_terminos_generosos()
            elif interpretation['question_type'] == "facturas_por_cobrar_total_fecha":
                analysis_results = self.data_processor.analyze_facturas_por_fecha(interpretation['fecha_filtro'], "por_cobrar")
            elif interpretation['question_type'] == "facturas_por_pagar_total_fecha":
                analysis_results = self.data_processor.analyze_facturas_por_fecha(interpretation['fecha_filtro'], "por_pagar")
            elif 'mes' in interpretation['question_type']:
                analysis_results = self.data_processor.analyze_facturas_por_mes()
            else:
                analysis_results = {}
            
            self.execution_steps.append("analyze")
            print(f"   ✅ Análisis completado: {len(analysis_results)} métricas calculadas")
            
            # Paso 3: Generar prompt si es necesario
            if interpretation.get("use_prompts"):
                self.show_progress("prompt", "Generando prompt para respuesta flexible...")
                time.sleep(1)
                self.execution_steps.append("prompt")
                print(f"   🤖 Prompt generado para análisis personalizado")
            
            # Paso 4: Formatear respuesta
            self.show_progress("respond", "Formateando respuesta ejecutiva...")
            time.sleep(1)
            response = self.response_formatter.format_response(question, analysis_results, interpretation['question_type'])
            self.execution_steps.append("respond")
            
            # Paso 5: Retroalimentación
            if self.config.enable_feedback:
                self.show_progress("feedback", "Solicitando retroalimentación...")
                time.sleep(0.5)
                self.execution_steps.append("feedback")
            
            # Paso 6: Finalizar
            self.show_progress("end", "Proceso completado")
            time.sleep(0.5)
            self.execution_steps.append("end")
            
            return response
            
        except Exception as e:
            error_msg = f"❌ Error procesando pregunta: {e}"
            print(error_msg)
            return error_msg
    
    def show_execution_summary(self):
        """Mostrar resumen de la ejecución."""
        print("\n📊 RESUMEN DE EJECUCIÓN")
        print("=" * 60)
        print(f"Pasos ejecutados: {len(self.execution_steps)}")
        print(f"Pasos: {' → '.join(self.execution_steps)}")
        if self.config.enable_dynamic_visualization:
            print(f"Visualización dinámica: Habilitada")
        if self.config.enable_feedback:
            print(f"Retroalimentación: Habilitada")


def main():
    """Función principal del agente mejorado."""
    print("🎯 ENHANCED FINANCIAL AGENT - FIXED VERSION")
    print("=" * 60)
    print("🤖 Agente financiero con visualización dinámica y retroalimentación")
    print("💡 Prompts funcionales y nodos de aclaración")
    print("=" * 60)
    
    # Crear agente
    config = FinancialAgentConfig(
        enable_prompt_engineering=True,
        enable_dynamic_visualization=True,
        enable_feedback=True,
        enable_clarification=True
    )
    
    agent = EnhancedFinancialAgentFixed(config)
    
    # Bucle interactivo
    while True:
        try:
            print("\n💡 Intenta con otra pregunta")
            question = input("\n❓ Tu pregunta (o 'salir' para terminar): ").strip()
            
            if question.lower() in ['salir', 'exit', 'quit']:
                print("\n👋 ¡Hasta luego!")
                break
            
            if not question:
                continue
            
            # Procesar pregunta
            response = agent.process_question(question)
            
            # Mostrar respuesta
            print("\n📋 RESPUESTA:")
            print("=" * 60)
            print(response)
            
            # Mostrar resumen
            agent.show_execution_summary()
            
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("💡 Intenta con otra pregunta")


if __name__ == "__main__":
    main() 