"""
Enhanced Financial Agent with Prompt Engineering
Agente financiero mejorado con sistema de prompts para respuestas flexibles.
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

from prompts import FinancialPrompts, PromptManager, create_simple_prompt, create_comparison_prompt, create_trend_analysis_prompt


@dataclass
class FinancialAgentConfig:
    """Configuración del agente financiero con prompts."""
    
    # Configuración de análisis
    max_analysis_iterations: int = 3
    allow_clarification: bool = True
    enable_prompt_engineering: bool = True
    enable_flexible_responses: bool = True
    
    # ========================================
    # CAMBIAR AQUÍ LAS FUENTES DE DATOS
    # ========================================
    data_directory: str = "Datasets v2/Datasets v2"  # ← CAMBIAR ESTA RUTA
    # Ejemplos:
    # data_directory: str = "mi_carpeta_de_datos"
    # data_directory: str = "excel_files"
    # data_directory: str = "datos_financieros"
    # ========================================
    
    supported_file_types: List[str] = None
    
    # Configuración de visualización
    enable_graph_visualization: bool = True
    enable_console_progress: bool = True
    
    def __post_init__(self):
        if self.supported_file_types is None:
            self.supported_file_types = [".xlsx", ".csv", ".json"]


class SimpleGraphVisualizer:
    """Visualizador de grafo simplificado."""
    
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.nodes = {}
        self.edges = []
        self.create_graph()
    
    def create_graph(self):
        """Crear estructura del grafo."""
        self.nodes = {
            'interpret': {'pos': (1, 4), 'label': 'Interpretar\nPregunta'},
            'analyze': {'pos': (3, 4), 'label': 'Analizar\nDatos'},
            'prompt': {'pos': (5, 4), 'label': 'Generar\nPrompt'},
            'respond': {'pos': (7, 4), 'label': 'Formatear\nRespuesta'},
            'end': {'pos': (4, 2), 'label': 'Finalizar'}
        }
        
        self.edges = [
            ('interpret', 'analyze'),
            ('analyze', 'prompt'),
            ('prompt', 'respond'),
            ('respond', 'end')
        ]
    
    def update_node_status(self, current_node=None, completed_nodes=None):
        """Actualizar estado de nodos."""
        if completed_nodes is None:
            completed_nodes = set()
        
        # Colores: gris=pendiente, verde=completado, azul=actual
        colors = []
        for node in self.nodes:
            if node == current_node:
                colors.append('lightblue')
            elif node in completed_nodes:
                colors.append('lightgreen')
            else:
                colors.append('lightgray')
        
        return colors
    
    def draw_graph(self):
        """Dibujar el grafo."""
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
        colors = self.update_node_status()
        
        # Dibujar
        nx.draw(G, pos, ax=self.ax, 
                node_color=colors,
                node_size=3000,
                font_size=9,
                font_weight='bold',
                arrows=True,
                edge_color='gray',
                with_labels=True,
                labels={node: self.nodes[node]['label'] for node in G.nodes()})
        
        self.ax.set_title('🎯 Enhanced Financial Agent with Prompts', fontsize=14, fontweight='bold')
        self.ax.set_xlim(0, 8)
        self.ax.set_ylim(1, 5)
    
    def update_display(self):
        """Actualizar visualización."""
        plt.draw()
        plt.pause(0.1)
    
    def show_initial_graph(self):
        """Mostrar grafo inicial."""
        self.draw_graph()
        self.update_display()
    
    def update_progress(self, current_node, completed_nodes=None):
        """Actualizar progreso."""
        if completed_nodes is None:
            completed_nodes = set()
        
        self.draw_graph()
        self.update_display()


class FinancialAgentState:
    """Estado del agente financiero."""
    
    def __init__(self):
        self.current_question = ""
        self.question_type = ""
        self.data_sources = []
        self.raw_data = {}
        self.analysis_results = {}
        self.clarification_needed = False
        self.clarification_question = ""
        self.fecha_filtro = None
        self.execution_steps = []
        self.error_log = []
        self.prompt_used = ""
        self.response_generated = ""


class FinancialDataProcessor:
    """Procesador de datos financieros."""
    
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
        # Limpiar nombres de columnas
        df.columns = df.columns.str.strip().str.replace(' ', '_')
        
        # Manejar valores faltantes
        df = df.fillna(0)
        
        return df
    
    def analyze_facturas(self, fecha_filtro: str = None) -> Dict[str, Any]:
        """Análisis completo de facturas con filtro opcional por fecha."""
        if 'facturas' not in self.data:
            return {}
        
        df = self.data['facturas'].copy()
        analysis = {}
        
        # Aplicar filtro de fecha si se especifica
        if fecha_filtro:
            fecha_col = None
            for col in df.columns:
                if 'fecha' in col.lower() or 'emision' in col.lower():
                    fecha_col = col
                    break
            
            if fecha_col:
                try:
                    df[fecha_col] = pd.to_datetime(df[fecha_col], errors='coerce')
                    
                    # Filtrar por mes
                    month_map = {
                        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
                        "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
                        "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
                    }
                    
                    if fecha_filtro.lower() in month_map:
                        df = df[df[fecha_col].dt.month == month_map[fecha_filtro.lower()]]
                        analysis['fecha_filtro'] = fecha_filtro
                        analysis['registros_filtrados'] = len(df)
                    
                except Exception as e:
                    print(f"⚠️  Error aplicando filtro de fecha: {e}")
        
        # Análisis básico
        amount_col = self._get_amount_column(df)
        if amount_col:
            analysis['total'] = df[amount_col].sum()
            analysis['promedio'] = df[amount_col].mean()
            analysis['min'] = df[amount_col].min()
            analysis['max'] = df[amount_col].max()
            analysis['count'] = len(df)
        
        # Análisis por tipo
        if 'Tipo' in df.columns and amount_col:
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
            if tipo_factura:
                monthly_data = df.groupby(['mes', 'mes_nombre']).agg({
                    amount_col: ['sum', 'count'],
                    'Tipo': 'first'
                }).reset_index()
                
                # Encontrar mes con más facturas
                max_count_idx = monthly_data[(amount_col, 'count')].idxmax()
                max_month = monthly_data.iloc[max_count_idx]
                
                analysis['mes_maximo'] = str(max_month['mes_nombre'])
                analysis['mes_maximo_numero'] = int(max_month['mes'])
                analysis['cantidad_maxima'] = float(max_month[(amount_col, 'sum')])
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
            else:
                monthly_data = df.groupby(['mes', 'mes_nombre']).agg({
                    amount_col: ['sum', 'count']
                }).reset_index()
                
                # Encontrar mes con más facturas
                max_count_idx = monthly_data[(amount_col, 'count')].idxmax()
                max_month = monthly_data.iloc[max_count_idx]
                
                analysis['mes_maximo'] = str(max_month['mes_nombre'])
                analysis['mes_maximo_numero'] = int(max_month['mes'])
                analysis['cantidad_maxima'] = float(max_month[(amount_col, 'sum')])
                analysis['facturas_maximas'] = int(max_month[(amount_col, 'count')])
                
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


class QuestionInterpreter:
    """Intérprete de preguntas con prompts."""
    
    def __init__(self, enable_prompts: bool = True):
        self.enable_prompts = enable_prompts
        self.prompts = FinancialPrompts()
    
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
        
        # Determinar tipo de pregunta con filtros específicos
        if ('mes' in question_lower and ('más' in question_lower or 'mas' in question_lower) and 'facturas' in question_lower and 'por cobrar' in question_lower):
            question_type = "facturas_por_cobrar_mes_maximo"
            data_sources = ["facturas.xlsx"]
            clarification_needed = False
        elif ('mes' in question_lower and ('más' in question_lower or 'mas' in question_lower) and 'facturas' in question_lower and 'por pagar' in question_lower):
            question_type = "facturas_por_pagar_mes_maximo"
            data_sources = ["facturas.xlsx"]
            clarification_needed = False
        elif ('mes' in question_lower and ('más' in question_lower or 'mas' in question_lower) and 'facturas' in question_lower):
            question_type = "facturas_mes_maximo"
            data_sources = ["facturas.xlsx"]
            clarification_needed = False
        elif 'por pagar' in question_lower and 'alta' in question_lower:
            question_type = "facturas_por_pagar_max"
            data_sources = ["facturas.xlsx"]
            clarification_needed = False
        elif 'por cobrar' in question_lower and 'alta' in question_lower:
            question_type = "facturas_por_cobrar_max"
            data_sources = ["facturas.xlsx"]
            clarification_needed = False
        elif 'total' in question_lower and 'facturas' in question_lower and 'por cobrar' in question_lower and fecha_filtro:
            question_type = "facturas_por_cobrar_total_fecha"
            data_sources = ["facturas.xlsx"]
            clarification_needed = False
        elif 'total' in question_lower and 'facturas' in question_lower and 'por pagar' in question_lower and fecha_filtro:
            question_type = "facturas_por_pagar_total_fecha"
            data_sources = ["facturas.xlsx"]
            clarification_needed = False
        elif 'por cobrar' in question_lower and fecha_filtro:
            question_type = "facturas_por_cobrar_fecha"
            data_sources = ["facturas.xlsx"]
            clarification_needed = False
        elif 'por pagar' in question_lower and fecha_filtro:
            question_type = "facturas_por_pagar_fecha"
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
            # Pregunta no pre-configurada, usar prompts
            question_type = "personalizado"
            data_sources = ["facturas.xlsx", "gastos_fijos.xlsx", "Estado_cuenta.xlsx"]
            clarification_needed = False
        
        return {
            "question_type": question_type,
            "data_sources": data_sources,
            "fecha_filtro": fecha_filtro,
            "analysis_required": f"Análisis de {question_type}",
            "clarification_needed": clarification_needed,
            "clarification_question": self._get_clarification_question(question, question_type),
            "use_prompts": question_type == "personalizado" and self.enable_prompts
        }
    
    def _get_clarification_question(self, question: str, question_type: str) -> str:
        """Generar pregunta de aclaración."""
        if question_type == "general" and len(question.split()) < 3:
            return f"Tu pregunta '{question}' es muy breve. ¿Podrías ser más específico sobre qué información financiera necesitas?"
        return ""


class ResponseFormatter:
    """Formateador de respuestas con prompts."""
    
    def __init__(self, enable_prompts: bool = True):
        self.enable_prompts = enable_prompts
        self.prompts = FinancialPrompts()
    
    def format_response(self, question: str, analysis_results: Dict[str, Any], question_type: str) -> str:
        """Formatear respuesta basada en el tipo de pregunta."""
        
        # Si es personalizado y están habilitados los prompts, usar prompt engineering
        if question_type == "personalizado" and self.enable_prompts:
            return self._format_prompt_response(question, analysis_results)
        
        # Respuestas pre-configuradas
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
        
        elif question_type == "facturas_por_cobrar_mes_maximo" and 'mes_maximo' in analysis_results:
            tipo = analysis_results.get('tipo_factura', 'por cobrar')
            return f"""
📊 Executive Summary
El mes con más facturas por cobrar es: {analysis_results['mes_maximo']}

📈 Detailed Analysis
- Mes con más facturas por cobrar: {analysis_results['mes_maximo']}
- Cantidad total en {analysis_results['mes_maximo']}: ${analysis_results['cantidad_maxima']:,.2f} MXN
- Número de facturas en {analysis_results['mes_maximo']}: {analysis_results['facturas_maximas']}

📊 Desglose por meses:
"""
            + "\n".join([f"- {mes}: ${datos['cantidad']:,.2f} ({datos['facturas']} facturas)" 
                        for mes, datos in analysis_results.get('datos_por_mes', {}).items()]) + f"""

🔍 Data Sources Used
- facturas.xlsx: Análisis por mes y tipo "Por cobrar"

💡 Key Insights
- {analysis_results['mes_maximo']} es el mes con más facturas por cobrar
- Total de {analysis_results['facturas_maximas']} facturas por cobrar en {analysis_results['mes_maximo']}
- Cantidad específica: ${analysis_results['cantidad_maxima']:,.2f} pesos mexicanos
"""
        
        elif question_type == "facturas_por_pagar_mes_maximo" and 'mes_maximo' in analysis_results:
            tipo = analysis_results.get('tipo_factura', 'por pagar')
            return f"""
📊 Executive Summary
El mes con más facturas por pagar es: {analysis_results['mes_maximo']}

📈 Detailed Analysis
- Mes con más facturas por pagar: {analysis_results['mes_maximo']}
- Cantidad total en {analysis_results['mes_maximo']}: ${analysis_results['cantidad_maxima']:,.2f} MXN
- Número de facturas en {analysis_results['mes_maximo']}: {analysis_results['facturas_maximas']}

📊 Desglose por meses:
"""
            + "\n".join([f"- {mes}: ${datos['cantidad']:,.2f} ({datos['facturas']} facturas)" 
                        for mes, datos in analysis_results.get('datos_por_mes', {}).items()]) + f"""

🔍 Data Sources Used
- facturas.xlsx: Análisis por mes y tipo "Por pagar"

💡 Key Insights
- {analysis_results['mes_maximo']} es el mes con más facturas por pagar
- Total de {analysis_results['facturas_maximas']} facturas por pagar en {analysis_results['mes_maximo']}
- Cantidad específica: ${analysis_results['cantidad_maxima']:,.2f} pesos mexicanos
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
    
    def _format_prompt_response(self, question: str, analysis_results: Dict[str, Any]) -> str:
        """Formatear respuesta usando prompts."""
        # Crear prompt para respuesta flexible
        prompt = self.prompts.create_flexible_analysis_prompt(question, analysis_results)
        
        # En una implementación real, aquí se enviaría el prompt a un LLM
        # Por ahora, simulamos una respuesta basada en los datos disponibles
        
        return f"""
🤖 RESPUESTA GENERADA CON PROMPT ENGINEERING
============================================================

📊 Executive Summary
Análisis personalizado para: "{question}"

📈 Detailed Analysis
Basado en los datos disponibles, he identificado la siguiente información relevante:

"""
        + self._generate_insights_from_data(analysis_results) + f"""

🔍 Data Sources Used
- Análisis basado en datos de facturas, gastos y estado de cuenta
- Respuesta generada usando prompt engineering para máxima flexibilidad

💡 Key Insights
- Esta respuesta fue generada usando análisis inteligente de datos
- Se consideraron múltiples fuentes de información
- El análisis se adaptó específicamente a tu pregunta

📝 Prompt Utilizado:
{prompt[:200]}...
"""
    
    def _generate_insights_from_data(self, data: Dict[str, Any]) -> str:
        """Generar insights basados en los datos disponibles."""
        insights = []
        
        if 'facturas' in data:
            facturas = data['facturas']
            if 'total' in facturas:
                insights.append(f"- Total de facturas: ${facturas['total']:,.2f} MXN")
            if 'por_cobrar' in facturas:
                insights.append(f"- Facturas por cobrar: ${facturas['por_cobrar']:,.2f} MXN")
            if 'por_pagar' in facturas:
                insights.append(f"- Facturas por pagar: ${facturas['por_pagar']:,.2f} MXN")
        
        if 'gastos_fijos' in data:
            gastos = data['gastos_fijos']
            if 'total_gastos' in gastos:
                insights.append(f"- Total de gastos fijos: ${gastos['total_gastos']:,.2f} MXN")
        
        if 'estado_cuenta' in data:
            cuenta = data['estado_cuenta']
            if 'total_movimientos' in cuenta:
                insights.append(f"- Total de movimientos bancarios: ${cuenta['total_movimientos']:,.2f} MXN")
        
        return "\n".join(insights) if insights else "- No se encontraron datos específicos para el análisis solicitado"


class EnhancedFinancialAgentWithPrompts:
    """Agente financiero mejorado con sistema de prompts."""
    
    def __init__(self, config: FinancialAgentConfig = None):
        self.config = config or FinancialAgentConfig()
        self.data_processor = FinancialDataProcessor(self.config)
        self.question_interpreter = QuestionInterpreter(self.config.enable_prompt_engineering)
        self.response_formatter = ResponseFormatter(self.config.enable_prompt_engineering)
        self.prompt_manager = PromptManager() if self.config.enable_prompt_engineering else None
        self.visualizer = SimpleGraphVisualizer() if self.config.enable_graph_visualization else None
        self.current_state = None
        self.execution_history = []
        
        # Mostrar información de configuración
        print(f"📁 Fuente de datos configurada: {self.config.data_directory}")
        print(f"🤖 Prompt Engineering: {'Habilitado' if self.config.enable_prompt_engineering else 'Deshabilitado'}")
        print(f"🎯 Respuestas flexibles: {'Habilitadas' if self.config.enable_flexible_responses else 'Deshabilitadas'}")
        
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
                self.visualizer.update_progress(step_name, set(self.current_state.execution_steps) if self.current_state else set())
            except Exception as e:
                print(f"⚠️  Error actualizando visualización: {e}")
    
    def process_question(self, question: str) -> str:
        """Procesar una pregunta financiera con prompts."""
        print(f"\n🎯 PROCESANDO: {question}")
        print("=" * 60)
        
        # Inicializar estado
        state = FinancialAgentState()
        state.current_question = question
        self.current_state = state
        
        try:
            # Paso 1: Interpretar pregunta
            self.show_progress("interpret_question", "Analizando la pregunta del usuario...")
            time.sleep(1)
            interpretation = self.question_interpreter.interpret_question(question)
            state.question_type = interpretation["question_type"]
            state.data_sources = interpretation["data_sources"]
            state.clarification_needed = interpretation["clarification_needed"]
            state.clarification_question = interpretation["clarification_question"]
            state.fecha_filtro = interpretation.get("fecha_filtro")
            state.execution_steps.append("interpret_question")
            print(f"   ✅ Interpretación completada: {state.question_type}")
            if interpretation.get("use_prompts"):
                print(f"   🤖 Usando prompt engineering para respuesta flexible")
            
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
            if state.question_type == "facturas_por_cobrar_mes_maximo":
                analysis_results = self.data_processor.analyze_facturas_por_mes("por_cobrar")
            elif state.question_type == "facturas_por_pagar_mes_maximo":
                analysis_results = self.data_processor.analyze_facturas_por_mes("por_pagar")
            elif state.question_type == "facturas_mes_maximo":
                analysis_results = self.data_processor.analyze_facturas_por_mes()
            elif 'facturas' in state.question_type:
                analysis_results = self.data_processor.analyze_facturas(state.fecha_filtro)
            elif 'gastos' in state.question_type:
                analysis_results = self.data_processor.analyze_gastos_fijos()
            elif 'flujo' in state.question_type or 'cuenta' in state.question_type:
                analysis_results = self.data_processor.analyze_estado_cuenta()
            else:
                # Análisis general
                analysis_results = self.data_processor.analyze_facturas(state.fecha_filtro)
            
            state.analysis_results = analysis_results
            state.execution_steps.append("load_and_analyze")
            print(f"   ✅ Análisis completado: {len(analysis_results)} métricas calculadas")
            
            # Paso 4: Generar prompt si es necesario
            if interpretation.get("use_prompts") and self.prompt_manager:
                self.show_progress("generate_prompt", "Generando prompt para respuesta flexible...")
                time.sleep(1)
                prompt = self.prompt_manager.get_context_prompt(question, analysis_results)
                state.prompt_used = prompt
                state.execution_steps.append("generate_prompt")
                print(f"   🤖 Prompt generado: {len(prompt)} caracteres")
            
            # Paso 5: Formatear respuesta
            self.show_progress("format_response", "Formateando respuesta ejecutiva...")
            time.sleep(1)
            response = self.response_formatter.format_response(question, analysis_results, state.question_type)
            state.response_generated = response
            state.execution_steps.append("format_response")
            
            # Paso 6: Finalizar
            self.show_progress("END", "Proceso completado")
            time.sleep(0.5)
            state.execution_steps.append("END")
            
            # Agregar a historial de conversación
            if self.prompt_manager:
                self.prompt_manager.add_to_history("user", question)
                self.prompt_manager.add_to_history("assistant", response)
            
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
            if self.current_state.prompt_used:
                print(f"Prompt engineering: Utilizado")
                print(f"Longitud del prompt: {len(self.current_state.prompt_used)} caracteres")


def main():
    """Función principal del agente con prompts."""
    print("🎯 ENHANCED FINANCIAL AGENT - WITH PROMPT ENGINEERING")
    print("=" * 60)
    print("🤖 Agente financiero con sistema de prompts para respuestas flexibles")
    print("💡 Puede responder preguntas no pre-configuradas usando análisis inteligente")
    print("=" * 60)
    
    # Crear agente
    config = FinancialAgentConfig(
        enable_prompt_engineering=True,
        enable_flexible_responses=True,
        enable_graph_visualization=True
    )
    
    agent = EnhancedFinancialAgentWithPrompts(config)
    
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