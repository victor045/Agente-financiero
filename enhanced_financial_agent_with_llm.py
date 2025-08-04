#!/usr/bin/env python3
"""
Enhanced Financial Agent with Real LLM Integration
Agente financiero mejorado con integración real de LLM para respuestas flexibles.
"""

import sys
import time
import json
import os
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

# Importar LLM
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
    LLM_AVAILABLE = True
except ImportError:
    print("⚠️  LLM no disponible. Instala: pip install langchain-openai")
    LLM_AVAILABLE = False

@dataclass
class FinancialAgentConfig:
    """Configuración del agente financiero mejorado."""

    # Configuración de LLM
    enable_llm: bool = True
    llm_model: str = "gpt-4o-mini"
    llm_max_tokens: int = 2048
    llm_temperature: float = 0.1
    
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
            'llm': {'pos': (7, 6), 'label': 'LLM\nAnálisis', 'color': 'lightgray'},
            'respond': {'pos': (9, 6), 'label': 'Formatear\nRespuesta', 'color': 'lightgray'},
            'feedback': {'pos': (5, 4), 'label': 'Retroalimentación\nUsuario', 'color': 'lightgray'},
            'end': {'pos': (5, 2), 'label': 'Finalizar', 'color': 'lightgray'}
        }

        self.edges = [
            ('interpret', 'clarify'),
            ('clarify', 'analyze'),
            ('analyze', 'llm'),
            ('llm', 'respond'),
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
        self.ax.set_title(f'🎯 Enhanced Financial Agent with LLM - {status}', fontsize=16, fontweight='bold')
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
        plt.show(block=False)

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

    def get_data_summary(self) -> Dict[str, Any]:
        """Obtener resumen de datos para LLM."""
        summary = {}
        
        for key, df in self.data.items():
            summary[key] = {
                'rows': len(df),
                'columns': list(df.columns),
                'sample_data': df.head(3).to_dict('records'),
                'numeric_columns': df.select_dtypes(include=['number']).columns.tolist()
            }
        
        # Agregar análisis específico para facturas
        if 'facturas' in self.data:
            facturas_df = self.data['facturas']
            summary['facturas_analysis'] = self._analyze_facturas_for_llm(facturas_df)
        
        return summary
    
    def _analyze_facturas_for_llm(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analizar facturas para proporcionar datos procesados al LLM."""
        analysis = {}
        
        try:
            # Encontrar columna de fecha
            fecha_col = None
            for col in df.columns:
                if 'fecha' in col.lower() or 'emision' in col.lower():
                    fecha_col = col
                    break
            
            if fecha_col:
                # Convertir a datetime
                df[fecha_col] = pd.to_datetime(df[fecha_col], errors='coerce')
                
                # Agregar columnas de mes
                df['mes'] = df[fecha_col].dt.month
                df['mes_nombre'] = df[fecha_col].dt.month_name()
                
                # Encontrar columna de monto correcta
                amount_col = self._get_amount_column(df)
                if amount_col:
                    monthly_data = df.groupby(['mes', 'mes_nombre']).agg({
                        amount_col: ['count', 'sum', 'mean']
                    }).reset_index()
                    
                    # Flatten column names
                    monthly_data.columns = ['mes', 'mes_nombre', 'facturas_count', 'monto_total', 'monto_promedio']
                    
                    # Encontrar mes con más y menos facturas
                    max_facturas_idx = monthly_data['facturas_count'].idxmax()
                    min_facturas_idx = monthly_data['facturas_count'].idxmin()
                    
                    analysis['mes_mas_facturas'] = {
                        'mes': str(monthly_data.iloc[max_facturas_idx]['mes_nombre']),
                        'facturas': int(monthly_data.iloc[max_facturas_idx]['facturas_count']),
                        'monto_total': float(monthly_data.iloc[max_facturas_idx]['monto_total'])
                    }
                    
                    analysis['mes_menos_facturas'] = {
                        'mes': str(monthly_data.iloc[min_facturas_idx]['mes_nombre']),
                        'facturas': int(monthly_data.iloc[min_facturas_idx]['facturas_count']),
                        'monto_total': float(monthly_data.iloc[min_facturas_idx]['monto_total'])
                    }
                    
                    # Análisis por tipo
                    if 'Tipo' in df.columns:
                        por_cobrar = df[df['Tipo'] == 'Por cobrar']
                        por_pagar = df[df['Tipo'] == 'Por pagar']
                        
                        analysis['por_cobrar'] = {
                            'total_facturas': len(por_cobrar),
                            'monto_total': float(por_cobrar[amount_col].sum()) if not por_cobrar.empty else 0,
                            'promedio': float(por_cobrar[amount_col].mean()) if not por_cobrar.empty else 0
                        }
                        
                        analysis['por_pagar'] = {
                            'total_facturas': len(por_pagar),
                            'monto_total': float(por_pagar[amount_col].sum()) if not por_pagar.empty else 0,
                            'promedio': float(por_pagar[amount_col].mean()) if not por_pagar.empty else 0
                        }
                    
                    # Datos mensuales completos
                    analysis['datos_mensuales'] = monthly_data.to_dict('records')
                    
                    # Estadísticas generales
                    analysis['estadisticas_generales'] = {
                        'total_facturas': len(df),
                        'monto_total': float(df[amount_col].sum()),
                        'promedio_factura': float(df[amount_col].mean()),
                        'factura_mas_alta': float(df[amount_col].max()),
                        'factura_mas_baja': float(df[amount_col].min())
                    }
            
        except Exception as e:
            print(f"⚠️  Error analizando facturas para LLM: {e}")
            analysis['error'] = str(e)
        
        return analysis
    
    def perform_additional_analysis(self, analysis_request: str, df: pd.DataFrame) -> Dict[str, Any]:
        """Realizar análisis adicional específico solicitado por el LLM."""
        analysis = {}
        
        try:
            amount_col = self._get_amount_column(df)
            if not amount_col:
                return {'error': 'No se encontró columna de monto'}
            
            # Encontrar columna de fecha
            fecha_col = None
            for col in df.columns:
                if 'fecha' in col.lower() or 'emision' in col.lower():
                    fecha_col = col
                    break
            
            if fecha_col:
                df[fecha_col] = pd.to_datetime(df[fecha_col], errors='coerce')
                df['mes'] = df[fecha_col].dt.month
                df['mes_nombre'] = df[fecha_col].dt.month_name()
            
            # Análisis específicos basados en la solicitud
            if 'proveedor' in analysis_request.lower():
                if 'Proveedor' in df.columns:
                    proveedor_analysis = df.groupby('Proveedor').agg({
                        amount_col: ['count', 'sum', 'mean']
                    }).reset_index()
                    proveedor_analysis.columns = ['proveedor', 'facturas_count', 'monto_total', 'monto_promedio']
                    analysis['proveedores'] = proveedor_analysis.to_dict('records')
            
            if 'terminos' in analysis_request.lower() or 'pago' in analysis_request.lower():
                if 'Términos de pago' in df.columns:
                    terminos_analysis = df.groupby('Términos de pago').agg({
                        amount_col: ['count', 'sum', 'mean']
                    }).reset_index()
                    terminos_analysis.columns = ['terminos', 'facturas_count', 'monto_total', 'monto_promedio']
                    analysis['terminos_pago'] = terminos_analysis.to_dict('records')
            
            if 'tendencia' in analysis_request.lower() or 'variacion' in analysis_request.lower():
                if fecha_col:
                    # Análisis de tendencias por mes
                    monthly_trend = df.groupby(['mes', 'mes_nombre']).agg({
                        amount_col: ['count', 'sum', 'mean']
                    }).reset_index()
                    monthly_trend.columns = ['mes', 'mes_nombre', 'facturas_count', 'monto_total', 'monto_promedio']
                    analysis['tendencia_mensual'] = monthly_trend.to_dict('records')
            
            if 'cliente' in analysis_request.lower():
                if 'Cliente' in df.columns:
                    cliente_analysis = df.groupby('Cliente').agg({
                        amount_col: ['count', 'sum', 'mean']
                    }).reset_index()
                    cliente_analysis.columns = ['cliente', 'facturas_count', 'monto_total', 'monto_promedio']
                    analysis['clientes'] = cliente_analysis.to_dict('records')
            
            # Análisis predictivo avanzado
            if 'futuro' in analysis_request.lower() or 'prediccion' in analysis_request.lower() or 'predicción' in analysis_request.lower():
                if fecha_col:
                    # Análisis de tendencias para predicción
                    monthly_trend = df.groupby(['mes', 'mes_nombre']).agg({
                        amount_col: ['count', 'sum', 'mean']
                    }).reset_index()
                    monthly_trend.columns = ['mes', 'mes_nombre', 'facturas_count', 'monto_total', 'monto_promedio']
                    
                    # Calcular tendencias
                    if len(monthly_trend) > 1:
                        # Tendencia de crecimiento
                        monthly_trend['tendencia_crecimiento'] = monthly_trend['monto_total'].pct_change()
                        monthly_trend['tendencia_facturas'] = monthly_trend['facturas_count'].pct_change()
                        
                        # Proyección simple (promedio de tendencias)
                        avg_growth = monthly_trend['tendencia_crecimiento'].mean()
                        avg_facturas_growth = monthly_trend['tendencia_facturas'].mean()
                        
                        analysis['prediccion'] = {
                            'tendencia_crecimiento_promedio': float(avg_growth) if not pd.isna(avg_growth) else 0,
                            'tendencia_facturas_promedio': float(avg_facturas_growth) if not pd.isna(avg_facturas_growth) else 0,
                            'datos_mensuales': monthly_trend.to_dict('records')
                        }
                    
                    analysis['tendencia_mensual'] = monthly_trend.to_dict('records')
            
        except Exception as e:
            print(f"⚠️  Error en análisis adicional: {e}")
            analysis['error'] = str(e)
        
        return analysis

    def _get_amount_column(self, df: pd.DataFrame) -> Optional[str]:
        """Obtener la columna de monto correcta."""
        amount_columns = ['Monto_MXN', 'Monto_(MXN)', 'Monto', 'Amount']
        for col in amount_columns:
            if col in df.columns:
                return col
        return None


class LLMAnalyzer:
    """Analizador usando LLM real."""

    def __init__(self, config: FinancialAgentConfig):
        self.config = config
        self.llm = None
        self.setup_llm()

    def setup_llm(self):
        """Configurar LLM."""
        if not LLM_AVAILABLE or not self.config.enable_llm:
            print("⚠️  LLM no disponible o deshabilitado")
            return

        try:
            # Intentar usar OpenAI
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                print("⚠️  OPENAI_API_KEY no encontrada. LLM deshabilitado.")
                return

            self.llm = ChatOpenAI(
                model=self.config.llm_model,
                max_tokens=self.config.llm_max_tokens,
                temperature=self.config.llm_temperature,
                api_key=api_key
            )
            print(f"✅ LLM configurado: {self.config.llm_model}")
        except Exception as e:
            print(f"❌ Error configurando LLM: {e}")

    def analyze_with_llm(self, question: str, data_summary: Dict[str, Any], conversation_context: str = "") -> str:
        """Analizar pregunta usando LLM."""
        if not self.llm:
            return "LLM no disponible para análisis avanzado."

        try:
            # Crear prompt para LLM
            system_prompt = f"""Eres un experto analista financiero especializado en análisis predictivo, tendencias y análisis de datos financieros. Analiza los datos financieros y responde la pregunta del usuario de manera completa y profesional.

DATOS DISPONIBLES:
{json.dumps(data_summary, indent=2, default=str)}

{conversation_context}

INSTRUCCIONES ESPECÍFICAS:
1. **Análisis de Datos**: Usa siempre los datos procesados de 'facturas_analysis' cuando estén disponibles
2. **Precisión**: Incluye montos exactos, fechas y números específicos cuando sea posible
3. **Contexto**: Proporciona contexto relevante sobre los datos analizados
4. **Insights**: Ofrece insights útiles y recomendaciones basadas en los datos
5. **Memoria**: Considera las conversaciones anteriores para proporcionar respuestas más contextualizadas
6. **Tipos de Preguntas**:
   - **Preguntas Específicas**: "factura más alta", "proveedor con mayor monto", "total en mayo"
   - **Preguntas Predictivas**: "tendencia futura", "comportamiento esperado", "proyecciones"
   - **Preguntas de Análisis**: "comparaciones", "distribuciones", "patrones"
   - **Preguntas de Tendencias**: "variaciones mensuales", "crecimientos", "comportamientos"
   - **Preguntas de Seguimiento**: "¿y qué hay de...?", "comparado con...", "además..."

7. **Formato de Respuesta**:
   - Executive Summary claro
   - Detailed Analysis con datos específicos
   - Data Sources Used
   - Key Insights y recomendaciones

8. **Análisis Predictivo**: Para preguntas sobre el futuro, usa patrones históricos y tendencias
9. **Análisis Adicional**: Si necesitas más datos, responde: "NEED_ANALYSIS: [descripción]"
10. **Consistencia**: Mantén consistencia con análisis anteriores cuando sea relevante

PREGUNTA DEL USUARIO: {question}

Responde de manera profesional, ejecutiva y completa, usando todos los datos disponibles y el contexto de conversaciones anteriores para proporcionar el mejor análisis posible."""

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=question)
            ]

            response = self.llm.invoke(messages)
            return response.content

        except Exception as e:
            print(f"❌ Error en análisis LLM: {e}")
            return f"Error en análisis LLM: {str(e)}"


class QuestionInterpreter:
    """Intérprete de preguntas mejorado."""

    def __init__(self, enable_clarification: bool = True):
        self.enable_clarification = enable_clarification

    def interpret_question(self, question: str) -> Dict[str, Any]:
        """Interpretar la pregunta del usuario - TODAS VAN AL LLM."""
        question_lower = question.lower()

        # Detectar filtros de fecha para contexto
        fecha_filtro = None
        month_names = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]

        for month in month_names:
            if month in question_lower:
                fecha_filtro = month
                break

        # TODAS LAS PREGUNTAS VAN AL LLM
        if len(question.split()) < 3:
            question_type = "general"
            data_sources = ["facturas.xlsx", "gastos_fijos.xlsx", "Estado_cuenta.xlsx"]
            clarification_needed = True
        else:
            question_type = "llm_analysis"
            data_sources = ["facturas.xlsx", "gastos_fijos.xlsx", "Estado_cuenta.xlsx"]
            clarification_needed = False

        return {
            "question_type": question_type,
            "data_sources": data_sources,
            "fecha_filtro": fecha_filtro,
            "clarification_needed": clarification_needed,
            "clarification_question": self._get_clarification_question(question, question_type),
            "use_llm": True  # SIEMPRE USAR LLM
        }

    def _get_clarification_question(self, question: str, question_type: str) -> str:
        """Generar pregunta de aclaración."""
        if question_type == "general" and len(question.split()) < 3:
            return f"Tu pregunta '{question}' es muy breve. ¿Podrías ser más específico sobre qué información financiera necesitas?"
        return ""


class EnhancedFinancialAgentWithLLM:
    """Agente financiero mejorado con integración de LLM real."""

    def __init__(self, config: FinancialAgentConfig = None):
        self.config = config or FinancialAgentConfig()
        self.data_processor = FinancialDataProcessor(self.config)
        self.question_interpreter = QuestionInterpreter(self.config.enable_clarification)
        self.llm_analyzer = LLMAnalyzer(self.config)
        self.visualizer = DynamicGraphVisualizer() if self.config.enable_dynamic_visualization else None
        self.execution_steps = []
        
        # Sistema de memoria y contexto
        self.conversation_history = []
        self.analysis_cache = {}
        self.user_preferences = {}

        # Mostrar información de configuración
        print(f"📁 Fuente de datos configurada: {self.config.data_directory}")
        print(f"🤖 LLM: {'Habilitado' if self.config.enable_llm and self.llm_analyzer.llm else 'Deshabilitado'}")
        print(f"🎯 Visualización dinámica: {'Habilitada' if self.config.enable_dynamic_visualization else 'Deshabilitada'}")
        print(f"💬 Retroalimentación: {'Habilitada' if self.config.enable_feedback else 'Deshabilitada'}")
        print(f"🧠 Memoria de conversación: Habilitada")

        # Mostrar grafo inicial
        if self.visualizer and self.config.enable_dynamic_visualization:
            print("🎯 Iniciando visualización dinámica del grafo...")
            self.visualizer.show_initial_graph()
            time.sleep(1)
    
    def add_to_conversation_history(self, question: str, response: str, analysis_type: str = "general"):
        """Agregar pregunta y respuesta al historial de conversación."""
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'response': response,
            'analysis_type': analysis_type
        })
        
        # Mantener solo las últimas 10 conversaciones
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
    
    def get_conversation_context(self) -> str:
        """Obtener contexto de conversaciones anteriores."""
        if not self.conversation_history:
            return ""
        
        context = "\n\nCONTEXTO DE CONVERSACIONES ANTERIORES:\n"
        for i, conv in enumerate(self.conversation_history[-3:], 1):  # Últimas 3 conversaciones
            context += f"{i}. Pregunta: {conv['question']}\n"
            context += f"   Respuesta: {conv['response'][:200]}...\n"
        
        return context
    
    def cache_analysis_result(self, question_type: str, result: str):
        """Cachear resultado de análisis para reutilización."""
        self.analysis_cache[question_type] = {
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_cached_analysis(self, question_type: str) -> str:
        """Obtener análisis cacheado si está disponible y reciente."""
        if question_type in self.analysis_cache:
            cache_time = datetime.fromisoformat(self.analysis_cache[question_type]['timestamp'])
            if (datetime.now() - cache_time).seconds < 300:  # 5 minutos
                return self.analysis_cache[question_type]['result']
        return None

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
        """Procesar una pregunta financiera con LLM."""
        print(f"\n🎯 PROCESANDO: {question}")
        print("=" * 60)

        try:
            # Paso 1: Interpretar pregunta
            self.show_progress("interpret", "Analizando la pregunta del usuario...")
            time.sleep(1)
            interpretation = self.question_interpreter.interpret_question(question)
            self.execution_steps.append("interpret")

            print(f"   ✅ Interpretación completada: {interpretation['question_type']}")
            if interpretation.get("use_llm"):
                print(f"   🤖 Usando LLM para análisis avanzado")

            # Verificar si necesita aclaración
            if interpretation['clarification_needed']:
                self.show_progress("clarify", "Solicitando aclaración...")
                self.execution_steps.append("clarify")
                return interpretation['clarification_question']

            # Paso 2: Cargar datos
            self.show_progress("analyze", "Cargando datos y realizando análisis...")
            time.sleep(1)
            data = self.data_processor.load_all_data()
            data_summary = self.data_processor.get_data_summary()
            self.execution_steps.append("analyze")

            print(f"   ✅ Análisis completado: {len(data_summary)} fuentes de datos")

            # Paso 3: Análisis con LLM si es necesario
            if interpretation.get("use_llm"):
                self.show_progress("llm", "Analizando con LLM...")
                time.sleep(1)
                llm_response = self.llm_analyzer.analyze_with_llm(question, data_summary)
                self.execution_steps.append("llm")
                print(f"   🤖 LLM completado: {len(llm_response)} caracteres")
                
                # Verificar si el LLM necesita análisis adicional
                if llm_response.startswith("NEED_ANALYSIS:"):
                    analysis_request = llm_response.replace("NEED_ANALYSIS:", "").strip()
                    print(f"   🔄 LLM solicita análisis adicional: {analysis_request}")
                    
                    # Retroceder al nodo de análisis
                    self.show_progress("analyze", f"Realizando análisis adicional: {analysis_request}")
                    
                    # Realizar análisis adicional
                    if 'facturas' in self.data_processor.data:
                        additional_analysis = self.data_processor.perform_additional_analysis(
                            analysis_request, 
                            self.data_processor.data['facturas']
                        )
                        
                        # Actualizar data_summary con el análisis adicional
                        data_summary['additional_analysis'] = additional_analysis
                        
                        # Volver a consultar al LLM con los datos adicionales
                        self.show_progress("llm", "Re-analizando con datos adicionales...")
                        llm_response = self.llm_analyzer.analyze_with_llm(question, data_summary)
                        print(f"   🤖 LLM re-análisis completado: {len(llm_response)} caracteres")

            # Paso 4: Formatear respuesta
            self.show_progress("respond", "Formateando respuesta ejecutiva...")
            time.sleep(1)

            # SIEMPRE USAR LLM
            response = self._format_llm_response(question, llm_response)

            self.execution_steps.append("respond")

            # Paso 5: Retroalimentación
            if self.config.enable_feedback:
                self.show_progress("feedback", "Solicitando retroalimentación...")
                time.sleep(1)
                self.execution_steps.append("feedback")

            # Paso 6: Agregar a memoria
            self.add_to_conversation_history(question, response, interpretation['question_type'])
            
            # Paso 7: Finalizar
            self.show_progress("end", "Proceso completado")
            time.sleep(1)
            self.execution_steps.append("end")

            return response

        except Exception as e:
            print(f"❌ Error procesando pregunta: {e}")
            return f"Error procesando la pregunta: {str(e)}"

    def _format_llm_response(self, question: str, llm_response: str) -> str:
        """Formatear respuesta del LLM."""
        return f"""
🤖 RESPUESTA GENERADA CON LLM REAL
============================================================

📊 Executive Summary
Análisis LLM para: "{question}"

📈 Detailed Analysis
{llm_response}

🔍 Data Sources Used
- Análisis basado en datos de facturas, gastos y estado de cuenta
- Respuesta generada usando LLM real para máxima precisión

💡 Key Insights
- Esta respuesta fue generada usando un modelo de lenguaje real
- Se consideraron múltiples fuentes de información
- El análisis se adaptó específicamente a tu pregunta
"""

    def _format_predefined_response(self, question: str, interpretation: Dict[str, Any]) -> str:
        """Formatear respuesta predefinida con análisis específico."""
        try:
            # Cargar datos para análisis específico
            data = self.data_processor.load_all_data()
            
            if interpretation['question_type'] == "factura_por_pagar_mas_alta":
                return self._analyze_factura_por_pagar_mas_alta(data)
            elif interpretation['question_type'] == "proveedor_mayor_monto":
                return self._analyze_proveedor_mayor_monto(data)
            elif interpretation['question_type'] == "facturas_por_cobrar_total_fecha":
                return self._analyze_facturas_por_cobrar_total_fecha(data, interpretation.get('fecha_filtro'))
            elif interpretation['question_type'] == "facturas_por_pagar_total_fecha":
                return self._analyze_facturas_por_pagar_total_fecha(data, interpretation.get('fecha_filtro'))
            elif interpretation['question_type'] == "facturas_mes_maximo":
                return self._analyze_facturas_mes_maximo(data)
            else:
                return f"""
📊 Executive Summary
Respuesta predefinida para: "{question}"

📈 Detailed Analysis
Tipo de pregunta: {interpretation['question_type']}
Fuentes de datos: {', '.join(interpretation['data_sources'])}

🔍 Data Sources Used
- Análisis basado en patrones predefinidos
- Respuesta generada usando lógica específica

💡 Key Insights
- Esta pregunta fue reconocida por el sistema
- Se usó análisis predefinido para mayor eficiencia
"""
        except Exception as e:
            return f"Error en análisis predefinido: {str(e)}"
    
    def _analyze_factura_por_pagar_mas_alta(self, data: Dict[str, pd.DataFrame]) -> str:
        """Analizar factura por pagar más alta."""
        if 'facturas' not in data:
            return "No se encontraron datos de facturas."
        
        df = data['facturas']
        amount_col = self.data_processor._get_amount_column(df)
        
        if not amount_col:
            return "No se encontró columna de monto en las facturas."
        
        # Filtrar facturas por pagar
        por_pagar = df[df['Tipo'] == 'Por pagar']
        
        if por_pagar.empty:
            return "No se encontraron facturas por pagar."
        
        # Encontrar la factura con mayor monto
        max_amount_idx = por_pagar[amount_col].idxmax()
        factura_max = por_pagar.loc[max_amount_idx]
        
        return f"""
📊 Executive Summary
Factura por pagar con mayor monto

📈 Detailed Analysis
La factura por pagar con mayor monto es:
- **Proveedor**: {factura_max.get('Proveedor', 'N/A')}
- **Monto**: ${factura_max[amount_col]:,.2f} MXN
- **Fecha**: {factura_max.get('Fecha de emisión', 'N/A')}
- **Términos de pago**: {factura_max.get('Términos de pago', 'N/A')}

🔍 Data Sources Used
- Análisis basado en datos de facturas por pagar
- Respuesta generada usando análisis específico

💡 Key Insights
- Esta factura representa el mayor compromiso financiero pendiente
- Se recomienda revisar los términos de pago para optimizar el flujo de caja
"""

    def _analyze_proveedor_mayor_monto(self, data: Dict[str, pd.DataFrame]) -> str:
        """Analizar proveedor con mayor monto total."""
        if 'facturas' not in data:
            return "No se encontraron datos de facturas."
        
        df = data['facturas']
        amount_col = self.data_processor._get_amount_column(df)
        
        if not amount_col:
            return "No se encontró columna de monto en las facturas."
        
        # Agrupar por proveedor y sumar montos
        if 'Proveedor' in df.columns:
            proveedor_totales = df.groupby('Proveedor')[amount_col].sum().sort_values(ascending=False)
        else:
            return "No se encontró columna 'Proveedor' en los datos."
        
        if proveedor_totales.empty:
            return "No se encontraron datos de proveedores."
        
        proveedor_max = proveedor_totales.index[0]
        monto_total = proveedor_totales.iloc[0]
        
        return f"""
📊 Executive Summary
Proveedor con mayor monto total de facturas

📈 Detailed Analysis
El proveedor con mayor monto total de facturas es:
- **Proveedor**: {proveedor_max}
- **Monto Total**: ${monto_total:,.2f} MXN
- **Número de facturas**: {len(df[df['Proveedor'] == proveedor_max])}

🔍 Data Sources Used
- Análisis basado en datos de facturas
- Respuesta generada usando análisis específico

💡 Key Insights
- Este proveedor representa el mayor volumen de negocio
- Se recomienda mantener una relación comercial estratégica
"""

    def _analyze_facturas_por_cobrar_total_fecha(self, data: Dict[str, pd.DataFrame], fecha_filtro: str) -> str:
        """Analizar total de facturas por cobrar en fecha específica."""
        if 'facturas' not in data:
            return "No se encontraron datos de facturas."
        
        df = data['facturas']
        amount_col = self.data_processor._get_amount_column(df)
        
        if not amount_col:
            return "No se encontró columna de monto en las facturas."
        
        # Filtrar por cobrar y fecha
        por_cobrar = df[df['Tipo'] == 'Por cobrar']
        
        if fecha_filtro:
            # Convertir fecha a datetime si es necesario
            fecha_col = None
            for col in df.columns:
                if 'fecha' in col.lower() or 'emision' in col.lower():
                    fecha_col = col
                    break
            
            if fecha_col:
                df_copy = df.copy()
                df_copy[fecha_col] = pd.to_datetime(df_copy[fecha_col], errors='coerce')
                df_copy['mes'] = df_copy[fecha_col].dt.month_name()
                por_cobrar = df_copy[df_copy['Tipo'] == 'Por cobrar']
                por_cobrar = por_cobrar[por_cobrar['mes'].str.contains(fecha_filtro, case=False, na=False)]
        
        if por_cobrar.empty:
            return f"No se encontraron facturas por cobrar para {fecha_filtro}."
        
        total_facturas = len(por_cobrar)
        monto_total = por_cobrar[amount_col].sum()
        
        return f"""
📊 Executive Summary
Total de facturas por cobrar en {fecha_filtro}

📈 Detailed Analysis
Para {fecha_filtro}:
- **Total de facturas por cobrar**: {total_facturas}
- **Monto total**: ${monto_total:,.2f} MXN
- **Promedio por factura**: ${monto_total/total_facturas:,.2f} MXN

🔍 Data Sources Used
- Análisis basado en datos de facturas por cobrar
- Respuesta generada usando análisis específico

💡 Key Insights
- Este monto representa el flujo de caja esperado
- Se recomienda seguimiento de cobranza
"""

    def _analyze_facturas_por_pagar_total_fecha(self, data: Dict[str, pd.DataFrame], fecha_filtro: str) -> str:
        """Analizar total de facturas por pagar en fecha específica."""
        if 'facturas' not in data:
            return "No se encontraron datos de facturas."
        
        df = data['facturas']
        amount_col = self.data_processor._get_amount_column(df)
        
        if not amount_col:
            return "No se encontró columna de monto en las facturas."
        
        # Filtrar por pagar y fecha
        por_pagar = df[df['Tipo'] == 'Por pagar']
        
        if fecha_filtro:
            # Convertir fecha a datetime si es necesario
            fecha_col = None
            for col in df.columns:
                if 'fecha' in col.lower() or 'emision' in col.lower():
                    fecha_col = col
                    break
            
            if fecha_col:
                df_copy = df.copy()
                df_copy[fecha_col] = pd.to_datetime(df_copy[fecha_col], errors='coerce')
                df_copy['mes'] = df_copy[fecha_col].dt.month_name()
                por_pagar = df_copy[df_copy['Tipo'] == 'Por pagar']
                por_pagar = por_pagar[por_pagar['mes'].str.contains(fecha_filtro, case=False, na=False)]
        
        if por_pagar.empty:
            return f"No se encontraron facturas por pagar para {fecha_filtro}."
        
        total_facturas = len(por_pagar)
        monto_total = por_pagar[amount_col].sum()
        
        return f"""
📊 Executive Summary
Total de facturas por pagar en {fecha_filtro}

📈 Detailed Analysis
Para {fecha_filtro}:
- **Total de facturas por pagar**: {total_facturas}
- **Monto total**: ${monto_total:,.2f} MXN
- **Promedio por factura**: ${monto_total/total_facturas:,.2f} MXN

🔍 Data Sources Used
- Análisis basado en datos de facturas por pagar
- Respuesta generada usando análisis específico

💡 Key Insights
- Este monto representa compromisos financieros pendientes
- Se recomienda planificación de flujo de caja
"""

    def _analyze_facturas_mes_maximo(self, data: Dict[str, pd.DataFrame]) -> str:
        """Analizar mes con más facturas."""
        if 'facturas' not in data:
            return "No se encontraron datos de facturas."
        
        df = data['facturas']
        amount_col = self.data_processor._get_amount_column(df)
        
        if not amount_col:
            return "No se encontró columna de monto en las facturas."
        
        # Encontrar columna de fecha
        fecha_col = None
        for col in df.columns:
            if 'fecha' in col.lower() or 'emision' in col.lower():
                fecha_col = col
                break
        
        if not fecha_col:
            return "No se encontró columna de fecha en las facturas."
        
        # Convertir fecha y agrupar por mes
        df[fecha_col] = pd.to_datetime(df[fecha_col], errors='coerce')
        df['mes'] = df[fecha_col].dt.month_name()
        
        monthly_stats = df.groupby('mes').agg({
            amount_col: ['count', 'sum', 'mean']
        }).reset_index()
        
        monthly_stats.columns = ['mes', 'facturas_count', 'monto_total', 'monto_promedio']
        
        # Encontrar mes con más facturas
        max_facturas_idx = monthly_stats['facturas_count'].idxmax()
        mes_max = monthly_stats.iloc[max_facturas_idx]
        
        return f"""
📊 Executive Summary
Mes con mayor número de facturas

📈 Detailed Analysis
El mes con más facturas es:
- **Mes**: {mes_max['mes']}
- **Número de facturas**: {int(mes_max['facturas_count'])}
- **Monto total**: ${mes_max['monto_total']:,.2f} MXN
- **Promedio por factura**: ${mes_max['monto_promedio']:,.2f} MXN

🔍 Data Sources Used
- Análisis basado en datos de facturas por mes
- Respuesta generada usando análisis específico

💡 Key Insights
- Este mes muestra la mayor actividad de facturación
- Se recomienda analizar los factores que impulsaron esta actividad
"""

    def show_execution_summary(self):
        """Mostrar resumen de ejecución."""
        print(f"\n📊 RESUMEN DE EJECUCIÓN")
        print("=" * 60)
        print(f"Pasos ejecutados: {len(self.execution_steps)}")
        print(f"Pasos: {' → '.join(self.execution_steps)}")
        print(f"Visualización dinámica: {'Habilitada' if self.config.enable_dynamic_visualization else 'Deshabilitada'}")
        print(f"Retroalimentación: {'Habilitada' if self.config.enable_feedback else 'Deshabilitada'}")
        print(f"Conversaciones en memoria: {len(self.conversation_history)}")
        print(f"\n💡 Intenta con otra pregunta")
    
    def export_conversation_report(self, filename: str = None) -> str:
        """Exportar reporte de conversación a archivo."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"financial_analysis_report_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("REPORTE DE ANÁLISIS FINANCIERO\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total de conversaciones: {len(self.conversation_history)}\n\n")
                
                for i, conv in enumerate(self.conversation_history, 1):
                    f.write(f"CONVERSACIÓN {i}\n")
                    f.write("-" * 30 + "\n")
                    f.write(f"Timestamp: {conv['timestamp']}\n")
                    f.write(f"Tipo: {conv['analysis_type']}\n")
                    f.write(f"Pregunta: {conv['question']}\n")
                    f.write(f"Respuesta: {conv['response']}\n\n")
                
                f.write("RESUMEN ESTADÍSTICO\n")
                f.write("-" * 30 + "\n")
                f.write(f"Análisis más frecuente: {self._get_most_frequent_analysis()}\n")
                f.write(f"Tiempo total de análisis: {len(self.conversation_history) * 30} segundos estimados\n")
            
            return f"✅ Reporte exportado a: {filename}"
        except Exception as e:
            return f"❌ Error exportando reporte: {str(e)}"
    
    def _get_most_frequent_analysis(self) -> str:
        """Obtener el tipo de análisis más frecuente."""
        if not self.conversation_history:
            return "N/A"
        
        analysis_types = [conv['analysis_type'] for conv in self.conversation_history]
        from collections import Counter
        most_common = Counter(analysis_types).most_common(1)
        return most_common[0][0] if most_common else "N/A"
    
    def clear_conversation_history(self):
        """Limpiar historial de conversación."""
        self.conversation_history = []
        self.analysis_cache = {}
        print("🧹 Historial de conversación limpiado")
    
    def show_conversation_stats(self):
        """Mostrar estadísticas de conversación."""
        print(f"\n📈 ESTADÍSTICAS DE CONVERSACIÓN")
        print("=" * 40)
        print(f"Total de conversaciones: {len(self.conversation_history)}")
        print(f"Análisis cacheados: {len(self.analysis_cache)}")
        
        if self.conversation_history:
            from collections import Counter
            analysis_types = [conv['analysis_type'] for conv in self.conversation_history]
            most_common = Counter(analysis_types).most_common(3)
            print(f"Tipos de análisis más frecuentes:")
            for analysis_type, count in most_common:
                print(f"  - {analysis_type}: {count} veces")


def main():
    """Función principal."""
    print("🎯 ENHANCED FINANCIAL AGENT WITH LLM")
    print("=" * 60)
    print("🤖 Agente financiero con integración real de LLM")
    print("💡 Análisis inteligente y respuestas flexibles")
    print("=" * 60)

    # Configurar agente
    config = FinancialAgentConfig(
        enable_llm=True,
        enable_dynamic_visualization=True,
        enable_feedback=True
    )

    agent = EnhancedFinancialAgentWithLLM(config)

    print("\n💡 Comandos disponibles:")
    print("  - Pregunta normal: Escribe tu pregunta")
    print("  - 'stats': Ver estadísticas de conversación")
    print("  - 'export': Exportar reporte de conversación")
    print("  - 'clear': Limpiar historial de conversación")
    print("  - 'salir': Terminar programa")
    print("\n❓ Tu pregunta o comando: ")

    while True:
        try:
            question = input().strip()
            
            if question.lower() in ['salir', 'exit', 'quit']:
                print("\n👋 ¡Hasta luego!")
                break
            
            if not question:
                print("💡 Intenta con otra pregunta")
                print("\n❓ Tu pregunta o comando: ")
                continue
            
            # Comandos especiales
            if question.lower() == 'stats':
                agent.show_conversation_stats()
                print("\n❓ Tu pregunta o comando: ")
                continue
            
            if question.lower() == 'export':
                result = agent.export_conversation_report()
                print(f"\n{result}")
                print("\n❓ Tu pregunta o comando: ")
                continue
            
            if question.lower() == 'clear':
                agent.clear_conversation_history()
                print("\n❓ Tu pregunta o comando: ")
                continue

            # Procesar pregunta
            response = agent.process_question(question)
            
            # Mostrar respuesta
            print(f"\n📋 RESPUESTA:")
            print("=" * 60)
            print(response)
            
            # Mostrar resumen
            agent.show_execution_summary()
            
            print("\n❓ Tu pregunta o comando: ")

        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except EOFError:
            print("\n❌ Error: EOF when reading a line")
            print("💡 Intenta con otra pregunta")
            print("\n❓ Tu pregunta o comando: ")


if __name__ == "__main__":
    main() 