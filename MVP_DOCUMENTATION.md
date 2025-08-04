# MVP Documentation - Financial Conversational Agent

## 🎯 Objetivo del Trial / Proyecto

Validar que el developer es capaz de construir un agente conversacional capaz de:

1. **Interpretar** una pregunta financiera en lenguaje natural usando un LLM
2. **Elegir** la fuente de datos más relevante entre múltiples archivos estructurados
3. **Ejecutar** un análisis cuantitativo correcto a partir de esos datos
4. **Responder** con claridad, precisión y trazabilidad

Esto representa una vertical funcional del producto que, en producción, ayudará a CEOs y CFOs a tomar decisiones financieras críticas desde una simple pregunta.

## 📋 Alcance del MVP Trial

### Cobertura Funcional Esperada

- ✅ **Lectura de múltiples archivos estructurados (Excel)**
- ✅ **Interpretación de una pregunta compleja en lenguaje natural (usando un LLM)**
- ✅ **Selección de la fuente de datos relevante (basado en metadata + análisis del contenido)**
- ✅ **Ejecución de un análisis financiero cuantitativo (no descriptivo)**
- ✅ **Respuesta estructurada con:**
  - Resumen ejecutivo (tipo BLUF)
  - Análisis detallado con datos
  - Trazabilidad completa (archivo + columnas usadas)
- ✅ **Código limpio, modular y documentado**

## 👥 Casos de Uso

### User Story Principal

> Como CEO, quiero escribir "¿Cómo variaron mis facturas por pagar y por cobrar en los últimos 2 meses?" para entender el impacto en mi flujo de caja y evaluar decisiones relacionadas con liquidez.

### Respuesta Esperada

El agente debería responder con:

```
## 📊 Executive Summary

Positive cash flow of $15,000 indicates healthy financial position.

## 📈 Detailed Analysis

### Cash Flow Analysis

- **Net Cash Flow**: $15,000
- **Total Inflows**: $45,000
- **Total Outflows**: $30,000

- **Accounts Receivable**: $25,000
- **Average Invoice**: $5,000

## 🔍 Data Sources Used

- **facturas.xlsx**: cliente, fecha, monto
- **Estado_cuenta.xlsx**: fecha, monto, tipo

## 💡 Key Insights & Recommendations

- Total accounts receivable: $25,000
- Average invoice amount: $5,000
- Net cash flow: $15,000
- Total inflows: $45,000
- Total outflows: $30,000

## 📋 Technical Details

Raw calculations and methodologies are available for verification in the analysis results.
```

## 🔧 Requerimientos Técnicos

### 1. Fuentes de Datos

El sistema maneja 3 archivos Excel simulados:

| Archivo | Contenido | Formato Esperado |
|---------|-----------|------------------|
| `facturacion.xlsx` | Facturas emitidas, fechas de vencimiento, cliente, monto | Columnas: Cliente, Fecha, Monto |
| `gastos_fijos.xlsx` | Egresos mensuales recurrentes | Columnas: Rubro, Fecha, Monto |
| `estado_cuenta_banco.xlsx` | Movimientos de cuenta bancaria | Columnas: Fecha, Monto, Tipo |

**Robustez ante errores comunes:**
- Fechas inconsistentes
- Nombres ruidosos
- Columnas sobrantes
- Valores faltantes

### 2. Arquitectura del Sistema

```
User Question → LangGraph Workflow → Structured Response
                ↓
    [Question Interpretation] → [Data Selection] → [Analysis] → [Formatting]
```

#### Componentes Implementados:

1. **Question Interpreter** (`interpret_question`)
   - Usa LLM para interpretar preguntas en lenguaje natural
   - Extrae tipo de análisis, período, métricas clave
   - Identifica fuentes de datos requeridas

2. **Data Selector** (`select_data_sources`)
   - Analiza archivos disponibles
   - Selecciona archivos relevantes basado en la pregunta
   - Identifica columnas específicas necesarias

3. **Data Loader** (`data_loader.py`)
   - Carga archivos Excel con manejo robusto de errores
   - Preprocesa datos (limpieza, normalización)
   - Maneja fechas inconsistentes y valores faltantes

4. **Financial Analyzer** (`financial_analyzer.py`)
   - Ejecuta cálculos cuantitativos específicos
   - Genera insights y recomendaciones
   - Mantiene trazabilidad completa

5. **Response Formatter** (`format_response`)
   - Estructura respuesta ejecutiva
   - Incluye análisis detallado
   - Proporciona trazabilidad y detalles técnicos

### 3. Análisis Financieros Soportados

- **Cash Flow Analysis**: Flujo de caja y liquidez
- **Expense Analysis**: Análisis de gastos por categoría
- **Revenue Analysis**: Análisis de ingresos por cliente
- **Comparison Analysis**: Comparaciones entre períodos
- **Trend Analysis**: Análisis de tendencias temporales

## 🏗️ Implementación Técnica

### Estado y Estructuras de Datos

```python
class FinancialQuestion(BaseModel):
    question_type: str
    time_period: Optional[str]
    metrics: List[str]
    data_sources: List[str]

class DataSourceSelection(BaseModel):
    selected_files: List[str]
    analysis_columns: Dict[str, List[str]]
    reasoning: str

class FinancialAnalysis(BaseModel):
    summary: str
    detailed_analysis: str
    data_traceability: Dict[str, List[str]]
    key_insights: List[str]
    calculations: Dict[str, Any]
```

### Flujo de Trabajo LangGraph

```python
def create_financial_agent() -> StateGraph:
    workflow = StateGraph(FinancialAgentState)
    
    # Add nodes
    workflow.add_node("interpret_question", interpret_question)
    workflow.add_node("select_data_sources", select_data_sources)
    workflow.add_node("load_and_analyze", load_and_analyze)
    workflow.add_node("format_response", format_response)
    
    # Set entry point and edges
    workflow.set_entry_point("interpret_question")
    workflow.add_edge("interpret_question", "select_data_sources")
    workflow.add_edge("select_data_sources", "load_and_analyze")
    workflow.add_edge("load_and_analyze", "format_response")
    workflow.add_edge("format_response", END)
    
    return workflow.compile()
```

### Manejo de Errores

1. **Data Quality Issues**:
   - Fechas inconsistentes → Conversión robusta con `pd.to_datetime`
   - Nombres de columnas ruidosos → Limpieza con regex
   - Valores faltantes → Estrategias específicas por tipo de archivo

2. **API Errors**:
   - Timeouts → Retry logic con backoff
   - Rate limits → Rate limiting implementado
   - Invalid responses → Fallback responses

3. **File System Errors**:
   - Missing files → Graceful degradation
   - Permission errors → Clear error messages
   - Corrupted files → Skip and continue

## 🧪 Testing y Validación

### Casos de Prueba Implementados

1. **Question Interpretation Tests**:
   - Preguntas en español
   - Preguntas con períodos específicos
   - Preguntas ambiguas

2. **Data Loading Tests**:
   - Archivos con errores de formato
   - Archivos con columnas faltantes
   - Archivos con datos inconsistentes

3. **Analysis Tests**:
   - Cálculos cuantitativos correctos
   - Trazabilidad completa
   - Insights relevantes

### Métricas de Éxito

- ✅ **Interpretación correcta** de preguntas financieras
- ✅ **Selección precisa** de fuentes de datos
- ✅ **Cálculos cuantitativos** correctos
- ✅ **Respuestas con trazabilidad** completa
- ✅ **Manejo robusto** de errores de datos
- ✅ **Código modular** y documentado

## 📊 Ejemplos de Uso

### Ejemplo 1: Análisis de Flujo de Caja

**Pregunta**: "¿Cómo variaron mis facturas por pagar y por cobrar en los últimos 2 meses?"

**Respuesta**:
```
## 📊 Executive Summary

Positive cash flow of $15,000 indicates healthy financial position.

## 📈 Detailed Analysis

### Cash Flow Analysis
- **Net Cash Flow**: $15,000
- **Total Inflows**: $45,000  
- **Total Outflows**: $30,000

### Accounts Receivable
- **Total Receivable**: $25,000
- **Average Invoice**: $5,000

## 🔍 Data Sources Used
- **facturas.xlsx**: cliente, fecha, monto
- **Estado_cuenta.xlsx**: fecha, monto, tipo

## 💡 Key Insights
- Strong positive cash flow indicates good liquidity
- Average invoice size suggests healthy client base
- Consider optimizing payment terms for better cash flow
```

### Ejemplo 2: Análisis de Gastos

**Pregunta**: "¿Cuáles son mis gastos fijos más altos?"

**Respuesta**:
```
## 📊 Executive Summary

Total fixed expenses: $12,500. Review categories for optimization opportunities.

## 📈 Detailed Analysis

### Expense Analysis
- **Total Expenses**: $12,500
- **Average Expense**: $2,500
- **Number of Expenses**: 5

### Expenses by Category
- **Rent**: $5,000 (1 item)
- **Utilities**: $3,000 (2 items)
- **Insurance**: $2,500 (1 item)
- **Software**: $2,000 (1 item)

## 🔍 Data Sources Used
- **gastos_fijos.xlsx**: rubro, fecha, monto

## 💡 Key Insights
- Rent represents 40% of fixed expenses
- Consider renegotiating rent terms
- Software costs are reasonable for business size
```

## 🚀 Deployment y Configuración

### Variables de Entorno

```bash
# Required
OPENAI_API_KEY=your-api-key

# Optional
FINANCIAL_AGENT_MODEL=gpt-4o-mini
FINANCIAL_AGENT_MAX_TOKENS=2000
FINANCIAL_AGENT_DATA_DIR=Datasets v2/Datasets v2
```

### Instalación

```bash
# Install dependencies
pip install -r requirements.txt

# Run setup
python financial_agent/setup.py

# Test the agent
python financial_agent/example_usage.py
```

## 📈 Próximos Pasos

### Mejoras Planificadas

1. **Análisis Avanzado**:
   - Análisis de tendencias temporales
   - Comparaciones entre períodos
   - Proyecciones financieras

2. **Interfaz de Usuario**:
   - Web interface con Streamlit
   - API REST para integración
   - Dashboard interactivo

3. **Funcionalidades Adicionales**:
   - Soporte para más formatos de archivo
   - Integración con sistemas contables
   - Alertas y notificaciones

### Escalabilidad

- **Manejo de archivos más grandes** con chunking
- **Caché de análisis** para preguntas repetidas
- **Procesamiento paralelo** para múltiples archivos
- **Base de datos** para persistencia de análisis

## 🎯 Conclusión

El MVP implementa exitosamente todos los requerimientos del trial:

- ✅ **Interpretación de preguntas** en lenguaje natural
- ✅ **Selección inteligente** de fuentes de datos
- ✅ **Análisis cuantitativo** robusto
- ✅ **Respuestas estructuradas** con trazabilidad
- ✅ **Código modular** y bien documentado
- ✅ **Manejo robusto** de errores

El agente está listo para ser utilizado por CEOs y CFOs para tomar decisiones financieras informadas basadas en preguntas simples en lenguaje natural. 