"""
Enhanced Financial Agent - Basado en las mejores prácticas de open_deep_research.
"""

import sys
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any, Literal, Union
from dataclasses import dataclass

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

try:
    import pandas as pd
    import numpy as np
    from pydantic import BaseModel, Field
    from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
    from langchain_core.runnables import RunnableConfig
    from langgraph.graph import START, END, StateGraph
    from langgraph.types import Command
    from langchain.chat_models import init_chat_model
except ImportError as e:
    print(f"⚠️  Error de importación: {e}")
    print("💡 Instala las dependencias: pip install pandas numpy pydantic langchain langgraph")
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
    
    # Modelos
    analysis_model: str = "openai:gpt-4o-mini"
    analysis_model_max_tokens: int = 8192
    
    # Configuración de análisis
    max_analysis_iterations: int = 3
    allow_clarification: bool = True
    max_structured_output_retries: int = 3
    
    # Configuración de datos
    data_directory: str = "Datasets v2/Datasets v2"
    supported_file_types: List[str] = None
    
    # Configuración de visualización
    enable_live_visualization: bool = True
    enable_console_progress: bool = True
    
    def __post_init__(self):
        if self.supported_file_types is None:
            self.supported_file_types = [".xlsx", ".csv", ".json"]


###################
# Structured Outputs
###################

class FinancialQuestion(BaseModel):
    """Estructura para interpretar preguntas financieras."""
    question_type: str = Field(
        description="Tipo de pregunta: 'facturas_por_pagar_max', 'facturas_por_cobrar_max', 'facturas_total', 'facturas_promedio', 'gastos_analisis', 'flujo_caja', 'general'"
    )
    data_sources_needed: List[str] = Field(
        description="Lista de archivos de datos necesarios: ['facturas.xlsx', 'gastos_fijos.xlsx', 'Estado_cuenta.xlsx']"
    )
    analysis_required: str = Field(
        description="Descripción detallada del análisis requerido"
    )
    clarification_needed: bool = Field(
        description="Si se necesita aclaración del usuario"
    )
    clarification_question: str = Field(
        description="Pregunta de aclaración si es necesaria"
    )


class DataSourceSelection(BaseModel):
    """Selección de fuentes de datos."""
    selected_files: List[str] = Field(
        description="Archivos seleccionados para análisis"
    )
    data_quality_notes: str = Field(
        description="Notas sobre la calidad de los datos"
    )
    preprocessing_required: bool = Field(
        description="Si se requiere preprocesamiento"
    )


class FinancialAnalysis(BaseModel):
    """Resultado del análisis financiero."""
    executive_summary: str = Field(
        description="Resumen ejecutivo de los hallazgos"
    )
    detailed_analysis: Dict[str, Any] = Field(
        description="Análisis detallado con métricas específicas"
    )
    key_insights: List[str] = Field(
        description="Insights clave del análisis"
    )
    data_sources_used: List[str] = Field(
        description="Fuentes de datos utilizadas"
    )
    specific_amounts: Dict[str, float] = Field(
        description="Cantidades específicas en pesos mexicanos"
    )


###################
# State Management
###################

class FinancialAgentState(BaseModel):
    """Estado del agente financiero."""
    messages: List[Any] = []
    current_question: Optional[str] = None
    question_interpretation: Optional[FinancialQuestion] = None
    data_sources: Optional[DataSourceSelection] = None
    analysis_results: Optional[FinancialAnalysis] = None
    raw_data: Dict[str, pd.DataFrame] = {}
    processed_data: Dict[str, Any] = {}
    visualization_state: Dict[str, Any] = {}
    error_log: List[str] = []


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
                
                # Detalles de la factura más alta por cobrar
                max_cobrar_idx = facturas_por_cobrar[amount_col].idxmax()
                analysis['por_cobrar_max_details'] = {
                    'folio': facturas_por_cobrar.loc[max_cobrar_idx, 'Folio_de_Factura'] if 'Folio_de_Factura' in facturas_por_cobrar.columns else 'N/A',
                    'cliente': facturas_por_cobrar.loc[max_cobrar_idx, 'Cliente_Proveedor'] if 'Cliente_Proveedor' in facturas_por_cobrar.columns else 'N/A',
                    'fecha': facturas_por_cobrar.loc[max_cobrar_idx, 'Fecha_de_Emision'] if 'Fecha_de_Emision' in facturas_por_cobrar.columns else 'N/A',
                    'monto': facturas_por_cobrar.loc[max_cobrar_idx, amount_col]
                }
            
            if not facturas_por_pagar.empty:
                analysis['por_pagar_max'] = facturas_por_pagar[amount_col].max()
                analysis['por_pagar_min'] = facturas_por_pagar[amount_col].min()
                analysis['por_pagar_count'] = len(facturas_por_pagar)
                analysis['por_pagar_promedio'] = facturas_por_pagar[amount_col].mean()
                
                # Detalles de la factura más alta por pagar
                max_pagar_idx = facturas_por_pagar[amount_col].idxmax()
                analysis['por_pagar_max_details'] = {
                    'folio': facturas_por_pagar.loc[max_pagar_idx, 'Folio_de_Factura'] if 'Folio_de_Factura' in facturas_por_pagar.columns else 'N/A',
                    'proveedor': facturas_por_pagar.loc[max_pagar_idx, 'Cliente_Proveedor'] if 'Cliente_Proveedor' in facturas_por_pagar.columns else 'N/A',
                    'fecha': facturas_por_pagar.loc[max_pagar_idx, 'Fecha_de_Emision'] if 'Fecha_de_Emision' in facturas_por_pagar.columns else 'N/A',
                    'monto': facturas_por_pagar.loc[max_pagar_idx, amount_col]
                }
        
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
# LangGraph Nodes
###################

async def interpret_question(state: FinancialAgentState, config: RunnableConfig) -> Command[Literal["select_data_sources", "clarify_question"]]:
    """Interpretar la pregunta del usuario."""
    config_obj = FinancialAgentConfig()
    
    # Configurar modelo
    model = init_chat_model(
        model=config_obj.analysis_model,
        max_tokens=config_obj.analysis_model_max_tokens
    ).with_structured_output(FinancialQuestion).with_retry(stop_after_attempt=config_obj.max_structured_output_retries)
    
    # Crear prompt
    prompt = f"""
Analiza la siguiente pregunta financiera y determina:
1. El tipo de análisis requerido
2. Las fuentes de datos necesarias
3. Si se necesita aclaración

Pregunta: {state.current_question}

Archivos disponibles:
- facturas.xlsx: Facturas por cobrar y por pagar
- gastos_fijos.xlsx: Gastos fijos mensuales
- Estado_cuenta.xlsx: Movimientos de cuenta

Tipos de análisis disponibles:
- facturas_por_pagar_max: Factura por pagar más alta
- facturas_por_cobrar_max: Factura por cobrar más alta
- facturas_total: Total de facturas emitidas
- facturas_promedio: Promedio de facturas
- gastos_analisis: Análisis de gastos fijos
- flujo_caja: Análisis de flujo de caja
- general: Análisis general
"""
    
    response = await model.ainvoke([HumanMessage(content=prompt)])
    
    # Actualizar estado
    state.question_interpretation = response
    
    if response.clarification_needed:
        return Command(goto="clarify_question")
    else:
        return Command(goto="select_data_sources")


async def clarify_question(state: FinancialAgentState, config: RunnableConfig) -> Command[Literal["interpret_question", "__end__"]]:
    """Solicitar aclaración al usuario."""
    if state.question_interpretation:
        clarification_msg = state.question_interpretation.clarification_question
        return Command(goto=END, update={"messages": [AIMessage(content=clarification_msg)]})
    return Command(goto="interpret_question")


async def select_data_sources(state: FinancialAgentState, config: RunnableConfig) -> Command[Literal["load_and_analyze"]]:
    """Seleccionar fuentes de datos relevantes."""
    config_obj = FinancialAgentConfig()
    
    # Configurar modelo
    model = init_chat_model(
        model=config_obj.analysis_model,
        max_tokens=config_obj.analysis_model_max_tokens
    ).with_structured_output(DataSourceSelection).with_retry(stop_after_attempt=config_obj.max_structured_output_retries)
    
    # Crear prompt
    prompt = f"""
Basado en la interpretación de la pregunta, selecciona las fuentes de datos necesarias:

Pregunta: {state.current_question}
Tipo de análisis: {state.question_interpretation.question_type if state.question_interpretation else 'general'}

Archivos disponibles:
- facturas.xlsx: Datos de facturas por cobrar y por pagar
- gastos_fijos.xlsx: Gastos fijos mensuales
- Estado_cuenta.xlsx: Movimientos de cuenta bancaria

Selecciona los archivos necesarios para el análisis.
"""
    
    response = await model.ainvoke([HumanMessage(content=prompt)])
    
    # Actualizar estado
    state.data_sources = response
    
    return Command(goto="load_and_analyze")


async def load_and_analyze(state: FinancialAgentState, config: RunnableConfig) -> Command[Literal["format_response"]]:
    """Cargar datos y realizar análisis."""
    config_obj = FinancialAgentConfig()
    
    # Inicializar procesador de datos
    processor = FinancialDataProcessor(config_obj)
    
    # Cargar datos
    state.raw_data = processor.load_all_data()
    
    # Realizar análisis según el tipo de pregunta
    if state.question_interpretation:
        question_type = state.question_interpretation.question_type
        
        if 'facturas' in question_type:
            analysis_results = processor.analyze_facturas()
        elif 'gastos' in question_type:
            analysis_results = processor.analyze_gastos_fijos()
        elif 'flujo' in question_type or 'cuenta' in question_type:
            analysis_results = processor.analyze_estado_cuenta()
        else:
            # Análisis general
            analysis_results = {
                'facturas': processor.analyze_facturas(),
                'gastos': processor.analyze_gastos_fijos(),
                'cuenta': processor.analyze_estado_cuenta()
            }
        
        # Configurar modelo para formatear respuesta
        model = init_chat_model(
            model=config_obj.analysis_model,
            max_tokens=config_obj.analysis_model_max_tokens
        ).with_structured_output(FinancialAnalysis).with_retry(stop_after_attempt=config_obj.max_structured_output_retries)
        
        # Crear prompt para formatear respuesta
        prompt = f"""
Formatea los resultados del análisis financiero:

Pregunta original: {state.current_question}
Tipo de análisis: {question_type}
Resultados del análisis: {analysis_results}

Crea una respuesta estructurada con:
1. Resumen ejecutivo
2. Análisis detallado
3. Insights clave
4. Fuentes de datos utilizadas
5. Cantidades específicas en pesos mexicanos
"""
        
        response = await model.ainvoke([HumanMessage(content=prompt)])
        state.analysis_results = response
    
    return Command(goto="format_response")


async def format_response(state: FinancialAgentState, config: RunnableConfig) -> Command[Literal["__end__"]]:
    """Formatear la respuesta final."""
    if state.analysis_results:
        # Crear respuesta formateada
        response_text = f"""
📊 Executive Summary
{state.analysis_results.executive_summary}

📈 Detailed Analysis
"""
        
        for key, value in state.analysis_results.detailed_analysis.items():
            if isinstance(value, (int, float)):
                response_text += f"- {key}: ${value:,.2f} MXN\n"
            else:
                response_text += f"- {key}: {value}\n"
        
        response_text += f"""
🔍 Data Sources Used
"""
        for source in state.analysis_results.data_sources_used:
            response_text += f"- {source}\n"
        
        response_text += f"""
💡 Key Insights
"""
        for insight in state.analysis_results.key_insights:
            response_text += f"- {insight}\n"
        
        if state.analysis_results.specific_amounts:
            response_text += f"""
💰 Cantidades Específicas
"""
            for key, amount in state.analysis_results.specific_amounts.items():
                response_text += f"- {key}: ${amount:,.2f} pesos mexicanos\n"
        
        return Command(goto=END, update={"messages": [AIMessage(content=response_text)]})
    
    return Command(goto=END)


###################
# Graph Construction
###################

def create_enhanced_financial_agent() -> StateGraph:
    """Crear el grafo del agente financiero mejorado."""
    
    # Crear grafo
    workflow = StateGraph(FinancialAgentState)
    
    # Agregar nodos
    workflow.add_node("interpret_question", interpret_question)
    workflow.add_node("clarify_question", clarify_question)
    workflow.add_node("select_data_sources", select_data_sources)
    workflow.add_node("load_and_analyze", load_and_analyze)
    workflow.add_node("format_response", format_response)
    
    # Agregar edges
    workflow.add_edge(START, "interpret_question")
    workflow.add_edge("interpret_question", "select_data_sources")
    workflow.add_edge("interpret_question", "clarify_question")
    workflow.add_edge("clarify_question", "interpret_question")
    workflow.add_edge("clarify_question", END)
    workflow.add_edge("select_data_sources", "load_and_analyze")
    workflow.add_edge("load_and_analyze", "format_response")
    workflow.add_edge("format_response", END)
    
    # Compilar grafo
    return workflow.compile()


###################
# Interactive Agent
###################

class EnhancedFinancialAgent:
    """Agente financiero mejorado con visualización y monitoreo."""
    
    def __init__(self, config: FinancialAgentConfig = None):
        self.config = config or FinancialAgentConfig()
        self.workflow = create_enhanced_financial_agent()
        self.data_processor = FinancialDataProcessor(self.config)
        self.current_state = None
        self.execution_history = []
    
    async def process_question(self, question: str) -> str:
        """Procesar una pregunta financiera."""
        print(f"\n🎯 PROCESANDO: {question}")
        print("=" * 60)
        
        # Inicializar estado
        initial_state = FinancialAgentState(
            current_question=question,
            messages=[HumanMessage(content=question)]
        )
        
        # Ejecutar workflow
        try:
            result = await self.workflow.ainvoke(initial_state)
            self.current_state = result
            
            # Extraer respuesta
            if result.messages:
                for message in reversed(result.messages):
                    if isinstance(message, AIMessage):
                        return message.content
            
            return "❌ No se pudo generar una respuesta."
            
        except Exception as e:
            print(f"❌ Error procesando pregunta: {e}")
            return f"❌ Error: {e}"
    
    def show_execution_summary(self):
        """Mostrar resumen de la ejecución."""
        if self.current_state:
            print("\n📊 RESUMEN DE EJECUCIÓN")
            print("=" * 60)
            print(f"Pregunta: {self.current_state.current_question}")
            print(f"Tipo de análisis: {self.current_state.question_interpretation.question_type if self.current_state.question_interpretation else 'N/A'}")
            print(f"Fuentes utilizadas: {self.current_state.data_sources.selected_files if self.current_state.data_sources else 'N/A'}")
            print(f"Archivos cargados: {list(self.current_state.raw_data.keys())}")
            print(f"Errores: {len(self.current_state.error_log)}")


###################
# Main Function
###################

async def main():
    """Función principal del agente mejorado."""
    print("🎯 ENHANCED FINANCIAL AGENT")
    print("=" * 60)
    print("💡 Basado en las mejores prácticas de open_deep_research")
    print("📊 Características:")
    print("   ✅ LangGraph con estado estructurado")
    print("   ✅ Configuración centralizada")
    print("   ✅ Procesamiento robusto de datos")
    print("   ✅ Análisis financiero especializado")
    print("   ✅ Respuestas estructuradas")
    print("   ✅ Manejo de errores")
    print("=" * 60)
    
    # Crear agente
    agent = EnhancedFinancialAgent()
    
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
            response = await agent.process_question(question)
            
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
    asyncio.run(main()) 