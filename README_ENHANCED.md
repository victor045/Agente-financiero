# 🎯 Enhanced Financial Agent

Un agente financiero mejorado basado en las mejores prácticas del proyecto `open_deep_research`, con visualización gráfica, retroalimentación y arquitectura LangGraph robusta.

## 🚀 Características Principales

### 📊 **Análisis Financiero Avanzado**
- **Interpretación inteligente** de preguntas financieras
- **Análisis especializado** por tipo de factura (por cobrar/por pagar)
- **Cálculos precisos** con cantidades específicas en pesos mexicanos
- **Procesamiento robusto** de datos Excel con limpieza automática
- **Múltiples tipos de análisis**: facturas, gastos fijos, flujo de caja

### 🏗️ **Arquitectura LangGraph**
- **Estado estructurado** con Pydantic para trazabilidad completa
- **Nodos especializados** para cada etapa del análisis
- **Configuración centralizada** para fácil personalización
- **Manejo de errores** robusto con logging detallado
- **Flujo de trabajo** optimizado basado en open_deep_research

### 🎨 **Visualización y Monitoreo**
- **LangGraph Studio** para visualización interactiva
- **Gráficos en tiempo real** con matplotlib y networkx
- **Progreso en consola** con timestamps y estados
- **Monitoreo de ejecución** con métricas detalladas
- **Debugging avanzado** con logs estructurados

## 📁 Estructura del Proyecto

```
financial_agent/
├── enhanced_financial_agent.py      # Agente principal mejorado
├── interactive_agent.py             # Agente interactivo original
├── graph_visualization_simple.py    # Visualización simple
├── graph_visualization_live.py      # Visualización en tiempo real
├── langgraph_studio_enhanced.py     # Configuración LangGraph Studio
├── demo_questions.json              # Preguntas de demostración
└── README_ENHANCED.md              # Este archivo
```

## 🛠️ Instalación y Configuración

### 1. **Dependencias Básicas**
```bash
pip install pandas numpy pydantic langchain langgraph matplotlib networkx
```

### 2. **Configuración de Datos**
Asegúrate de tener los archivos Excel en `Datasets v2/Datasets v2/`:
- `facturas.xlsx` - Facturas por cobrar y por pagar
- `gastos_fijos.xlsx` - Gastos fijos mensuales
- `Estado_cuenta.xlsx` - Movimientos de cuenta

### 3. **Variables de Entorno**
Crea un archivo `.env` con tus API keys:
```bash
OPENAI_API_KEY=tu_api_key_aqui
```

## 🎯 Uso del Agente

### **Agente Mejorado (Recomendado)**
```bash
python3 financial_agent/enhanced_financial_agent.py
```

**Características:**
- ✅ Estado estructurado con Pydantic
- ✅ Configuración centralizada
- ✅ Procesamiento robusto de datos
- ✅ Análisis financiero especializado
- ✅ Respuestas estructuradas
- ✅ Manejo de errores avanzado

### **Agente Interactivo Original**
```bash
python3 financial_agent/interactive_agent.py
```

### **Visualización Simple**
```bash
python3 financial_agent/graph_visualization_simple.py
```

### **Visualización en Tiempo Real**
```bash
python3 financial_agent/graph_visualization_live.py
```

## 🎨 Visualización con LangGraph Studio

### **Configuración Rápida**
```bash
python3 financial_agent/langgraph_studio_enhanced.py
```

### **URLs Disponibles**
- 🎨 **Studio UI**: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- 📚 **API Docs**: http://127.0.0.1:2024/docs
- 🚀 **API**: http://127.0.0.1:2024

### **Características de Studio**
- ✅ Visualización interactiva del grafo
- ✅ Testing de nodos individuales
- ✅ Monitoreo de ejecuciones en tiempo real
- ✅ Debugging de errores
- ✅ Exportación de resultados
- ✅ Análisis de rendimiento

## 📊 Tipos de Análisis Disponibles

### **Análisis de Facturas**
- `facturas_por_pagar_max` - Factura por pagar más alta
- `facturas_por_cobrar_max` - Factura por cobrar más alta
- `facturas_total` - Total de facturas emitidas
- `facturas_promedio` - Promedio de facturas

### **Análisis de Gastos**
- `gastos_analisis` - Análisis de gastos fijos por categoría

### **Análisis de Flujo de Caja**
- `flujo_caja` - Análisis de movimientos de cuenta

### **Análisis General**
- `general` - Análisis completo de todos los datos

## 🔧 Nodos del Grafo LangGraph

### **1. interpret_question**
- **Función**: Interpretar preguntas financieras
- **Entrada**: Pregunta del usuario
- **Salida**: Tipo de análisis y fuentes de datos necesarias
- **Características**: Análisis semántico con LLM

### **2. select_data_sources**
- **Función**: Seleccionar archivos relevantes
- **Entrada**: Interpretación de la pregunta
- **Salida**: Lista de archivos a procesar
- **Características**: Selección inteligente de fuentes

### **3. load_and_analyze**
- **Función**: Cargar y analizar datos
- **Entrada**: Archivos seleccionados
- **Salida**: Resultados del análisis
- **Características**: Procesamiento robusto con pandas

### **4. format_response**
- **Función**: Formatear respuesta ejecutiva
- **Entrada**: Resultados del análisis
- **Salida**: Respuesta estructurada
- **Características**: Formato ejecutivo con insights

### **5. clarify_question**
- **Función**: Solicitar aclaraciones
- **Entrada**: Pregunta ambigua
- **Salida**: Pregunta de aclaración
- **Características**: Interacción con el usuario

## 📈 Ejemplos de Preguntas

### **Preguntas Específicas**
```bash
❓ ¿Cuál es la factura por pagar más alta?
❓ ¿Cuál es la factura por cobrar más alta?
❓ ¿Cuál es el total de facturas emitidas?
❓ ¿Cuál es el promedio de facturas por cobrar?
```

### **Preguntas de Análisis**
```bash
❓ ¿Cuáles son los gastos fijos más altos?
❓ ¿Cómo está el flujo de caja?
❓ ¿Cuál es el estado financiero general?
```

## 🎨 Opciones de Visualización

### **1. LangGraph Studio (Recomendado)**
- 🌐 Visualización interactiva del grafo
- 🧪 Testing de nodos individuales
- 📊 Monitoreo en tiempo real
- 🔧 Debugging avanzado

### **2. Visualización Simple**
- 📊 Gráficos estáticos con matplotlib
- 🎯 Colores dinámicos por estado
- 📋 Leyenda explicativa
- 💾 Exportación a PNG

### **3. Visualización en Tiempo Real**
- ⚡ Actualización en tiempo real
- 🔴 Nodos activos en rojo
- 🟢 Nodos completados en verde
- ⏱️ Timestamps de ejecución

### **4. Progreso en Consola**
- 📝 Logs detallados
- 🕐 Timestamps precisos
- 📊 Métricas de ejecución
- ❌ Manejo de errores

## 🔧 Configuración Avanzada

### **Personalización del Agente**
```python
from financial_agent.enhanced_financial_agent import FinancialAgentConfig, EnhancedFinancialAgent

# Configuración personalizada
config = FinancialAgentConfig(
    analysis_model="openai:gpt-4o",
    analysis_model_max_tokens=16384,
    max_analysis_iterations=5,
    enable_live_visualization=True
)

# Crear agente con configuración personalizada
agent = EnhancedFinancialAgent(config)
```

### **Tipos de Modelos Soportados**
- `openai:gpt-4o-mini` (recomendado)
- `openai:gpt-4o`
- `openai:gpt-4-turbo`
- `anthropic:claude-3-sonnet`
- `anthropic:claude-3-haiku`

## 📊 Mejoras Basadas en open_deep_research

### **🏗️ Arquitectura**
- ✅ **Estado estructurado** con Pydantic para trazabilidad
- ✅ **Configuración centralizada** para fácil personalización
- ✅ **Procesamiento robusto** de datos con manejo de errores
- ✅ **Nodos especializados** para cada etapa del análisis

### **📈 Análisis**
- ✅ **Interpretación inteligente** de preguntas financieras
- ✅ **Análisis especializado** por tipo de dato
- ✅ **Cálculos precisos** con cantidades específicas
- ✅ **Insights ejecutivos** con contexto relevante

### **🎨 Visualización**
- ✅ **LangGraph Studio** para visualización interactiva
- ✅ **Gráficos en tiempo real** con matplotlib
- ✅ **Monitoreo de ejecución** con métricas detalladas
- ✅ **Debugging avanzado** con logs estructurados

### **🔧 Configuración**
- ✅ **Múltiples modelos** para diferentes tareas
- ✅ **Configuración flexible** via environment variables
- ✅ **Manejo de errores** robusto con retry logic
- ✅ **Logging detallado** para debugging

## 🚀 Próximas Mejoras

### **Funcionalidades Planificadas**
- 🔄 **Análisis temporal** con tendencias y predicciones
- 📊 **Reportes ejecutivos** automáticos
- 🔗 **Integración con APIs** bancarias
- 🤖 **Agentes especializados** por tipo de análisis
- 📱 **Interfaz web** para usuarios no técnicos

### **Optimizaciones Técnicas**
- ⚡ **Procesamiento paralelo** para análisis complejos
- 💾 **Caché inteligente** para consultas repetidas
- 🔒 **Seguridad mejorada** para datos sensibles
- 📈 **Métricas de rendimiento** avanzadas

## 🤝 Contribuciones

### **Cómo Contribuir**
1. Fork el repositorio
2. Crea una rama para tu feature
3. Implementa las mejoras
4. Agrega tests
5. Envía un pull request

### **Áreas de Mejora**
- 📊 Nuevos tipos de análisis financiero
- 🎨 Mejoras en visualización
- 🔧 Optimizaciones de rendimiento
- 📚 Documentación adicional

## 📄 Licencia

Este proyecto está basado en las mejores prácticas de `open_deep_research` y está disponible bajo la misma licencia.

## 🙏 Agradecimientos

- **LangChain AI** por el proyecto `open_deep_research`
- **LangGraph** por el framework de visualización
- **Pandas** por el procesamiento robusto de datos
- **Matplotlib** por las capacidades de visualización

---

**🎯 Enhanced Financial Agent** - Transformando el análisis financiero con IA avanzada y visualización interactiva. 