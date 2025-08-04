# 🤖 Financial Conversational Agent v2.0

Un agente conversacional inteligente para análisis financiero construido con LangGraph que interpreta preguntas en lenguaje natural, selecciona fuentes de datos relevantes y ejecuta análisis financieros cuantitativos con **memoria contextual** y **análisis predictivo**.

## 🎯 Objetivo del Proyecto

Este proyecto valida la capacidad de construir un agente conversacional que puede:

- **Interpretar** preguntas financieras en lenguaje natural usando LLMs avanzados
- **Seleccionar** la fuente de datos más relevante entre múltiples archivos estructurados
- **Ejecutar** análisis cuantitativos correctos a partir de esos datos
- **Responder** con claridad, precisión y trazabilidad completa
- **Recordar** conversaciones anteriores para contexto
- **Predecir** tendencias futuras basadas en datos históricos
- **Exportar** reportes profesionales de análisis

## 🚀 Nuevas Funcionalidades v2.0

### 🧠 **Sistema de Memoria y Contexto**
- **Historial de conversaciones** (últimas 10)
- **Contexto de conversaciones anteriores** en el prompt
- **Memoria de análisis** para respuestas más inteligentes
- **Consistencia** entre respuestas relacionadas

### 🤖 **Sistema 100% LLM**
- **Eliminamos respuestas predefinidas** problemáticas
- **Todas las preguntas van al LLM** para mayor flexibilidad
- **Sin errores de columnas** o datos faltantes
- **Respuestas consistentes** y profesionales

### 📊 **Análisis Predictivo**
- **Tendencias históricas** para proyecciones futuras
- **Análisis de patrones** mensuales
- **Insights de comportamiento** de proveedores
- **Recomendaciones estratégicas**

### 🔄 **Sistema de Retroalimentación**
- **Análisis adicional** cuando el LLM lo solicita
- **Retroceso al nodo de análisis** para datos específicos
- **Re-análisis** con información adicional

### 📈 **Funcionalidades Avanzadas**
- **Comandos especiales**: `stats`, `export`, `clear`
- **Exportación de reportes** en formato texto
- **Estadísticas de conversación** detalladas
- **Gestión de memoria** (limpiar historial)

## 🏗️ Arquitectura Mejorada

El agente utiliza LangGraph para crear un flujo de trabajo estructurado con memoria:

```
User Question → Question Interpretation → Data Source Selection → Data Loading → Financial Analysis → LLM Analysis → Response Formatting → Memory Storage
```

### Componentes Principales

1. **Question Interpreter**: Interpreta preguntas en lenguaje natural usando LLMs
2. **Data Selector**: Selecciona archivos Excel relevantes basado en la pregunta
3. **Data Loader**: Carga y preprocesa archivos Excel con manejo robusto de errores
4. **Financial Analyzer**: Ejecuta análisis financieros específicos
5. **LLM Analyzer**: Análisis inteligente con memoria contextual
6. **Response Formatter**: Formatea respuestas con trazabilidad completa
7. **Memory Manager**: Gestiona historial de conversaciones y contexto

## 📊 Fuentes de Datos

El sistema maneja 3 archivos Excel simulados:

| Archivo | Contenido | Columnas Esperadas |
|---------|-----------|-------------------|
| `facturas.xlsx` | Facturas emitidas, fechas de vencimiento, cliente, monto | Cliente, Fecha, Monto |
| `gastos_fijos.xlsx` | Egresos mensuales recurrentes | Rubro, Fecha, Monto |
| `Estado_cuenta.xlsx` | Movimientos de cuenta bancaria | Fecha, Monto, Tipo |

## 🚀 Instalación

1. **Clonar el repositorio**:
```bash
git clone <repository-url>
cd financial_agent
```

2. **Instalar dependencias**:
```bash
pip install -r requirements_llm.txt
```

3. **Configurar variables de entorno**:
```bash
export OPENAI_API_KEY="tu-api-key-de-openai"
```

## 💻 Uso Básico

### Ejecutar el Agente Interactivo

```bash
python3 enhanced_financial_agent_with_llm.py
```

### Comandos Disponibles

- **Pregunta normal**: Escribe tu pregunta financiera
- **`stats`**: Ver estadísticas de conversación
- **`export`**: Exportar reporte de conversación
- **`clear`**: Limpiar historial de conversación
- **`salir`**: Terminar programa

### Ejemplo de Uso

```python
from enhanced_financial_agent_with_llm import EnhancedFinancialAgentWithLLM, FinancialAgentConfig

# Configurar el agente
config = FinancialAgentConfig(
    enable_llm=True,
    enable_dynamic_visualization=True,
    enable_feedback=True
)

agent = EnhancedFinancialAgentWithLLM(config)

# Preguntas del PRD
questions = [
    "¿Cómo variaron mis facturas por pagar y por cobrar en los últimos 2 meses?",
    "¿Cuál es el total de facturas por cobrar emitidas en mayo?",
    "¿De las facturas por pagar cuál es la más alta?",
    "¿Cuál es el proveedor con mayor monto total?",
    "¿Cuál fue el mes con más facturas?",
    "¿Comparado con mayo, cómo se comportó junio?"
]

for question in questions:
    response = agent.process_question(question)
    print(f"Pregunta: {question}")
    print(f"Respuesta: {response[:200]}...")
    print("-" * 50)
```

## 🧪 Testing

### Test Básico
```bash
python3 test_solo_llm.py
```

### Test de Mejoras Avanzadas
```bash
python3 test_mejoras_avanzadas.py
```

### Test de Retroalimentación
```bash
python3 test_retroalimentacion_especifica.py
```

## 📋 Tipos de Preguntas Soportadas

### 🔍 **Preguntas Específicas**
- "¿Cuál es la factura más alta?"
- "¿Cuál es el proveedor con mayor monto?"
- "¿Cuál es el total de facturas en mayo?"

### 📈 **Preguntas Predictivas**
- "¿Cuál será el comportamiento esperado?"
- "¿Qué tendencias se observan?"
- "¿Cómo se proyecta el futuro?"

### 📊 **Preguntas de Análisis**
- "¿Cuáles son las comparaciones?"
- "¿Cómo se distribuyen los datos?"
- "¿Qué patrones se identifican?"

### 📅 **Preguntas de Tendencias**
- "¿Cómo variaron los datos mensualmente?"
- "¿Cuál fue el crecimiento?"
- "¿Qué comportamientos se observan?"

### 🔄 **Preguntas de Seguimiento**
- "¿Y qué hay de...?"
- "¿Comparado con...?"
- "¿Además...?"

## 🎯 Características Destacadas

### ✅ **100% LLM**
- Todas las preguntas usan análisis inteligente
- Sin limitaciones de preguntas predefinidas
- Respuestas flexibles y contextuales

### ✅ **Memoria Contextual**
- Hasta 10 conversaciones en contexto
- Respuestas coherentes entre sesiones
- Análisis basado en conversaciones anteriores

### ✅ **Análisis Predictivo**
- Proyecciones basadas en datos históricos
- Tendencias y patrones identificados
- Recomendaciones estratégicas

### ✅ **Retroalimentación Inteligente**
- Análisis adicional cuando es necesario
- Re-análisis con datos específicos
- Mejora continua de respuestas

### ✅ **Exportación Profesional**
- Reportes completos en formato texto
- Estadísticas detalladas de conversación
- Trazabilidad completa de análisis

## 📊 Estadísticas del Sistema

- ✅ **100% LLM**: Todas las preguntas usan análisis inteligente
- ✅ **Memoria**: Hasta 10 conversaciones en contexto
- ✅ **Retroalimentación**: Análisis adicional cuando es necesario
- ✅ **Exportación**: Reportes completos en formato texto
- ✅ **Comandos**: 4 comandos especiales disponibles

## 🔧 Configuración

### Cambiar Fuentes de Datos

Edita el archivo `enhanced_financial_agent_with_llm.py`:

```python
config = FinancialAgentConfig(
    data_directory="tu/ruta/a/datos",  # Cambiar aquí
    enable_llm=True,
    enable_dynamic_visualization=True,
    enable_feedback=True
)
```

### Configuración de LLM

```python
config = FinancialAgentConfig(
    llm_model="gpt-4o-mini",  # Modelo de LLM
    llm_max_tokens=2048,       # Tokens máximos
    llm_temperature=0.1,       # Temperatura (creatividad)
    enable_llm=True
)
```

## 📈 Ejemplos de Respuestas

### Pregunta: "¿Cuál fue el mes con más facturas?"

```
📊 Executive Summary
El mes con más facturas emitidas fue mayo, con 23 facturas y un monto total de $287,450.23 MXN.

📈 Detailed Analysis
- Mayo: 23 facturas, $287,450.23 MXN
- Junio: 17 facturas, $151,752.00 MXN
- Promedio por factura en mayo: $12,497.84 MXN

🔍 Data Sources Used
- facturas.xlsx: Análisis mensual de facturación

💡 Key Insights
- Mayo muestra la mayor actividad de facturación
- Se recomienda analizar factores que impulsaron esta actividad
```

### Pregunta: "¿Comparado con mayo, cómo se comportó junio?"

```
📊 Executive Summary
Junio mostró una disminución del 26% en número de facturas y 47% en monto total comparado con mayo.

📈 Detailed Analysis
- Mayo: 23 facturas, $287,450.23 MXN
- Junio: 17 facturas, $151,752.00 MXN
- Diferencia: -6 facturas (-26%), -$135,698.23 (-47%)

🔍 Data Sources Used
- facturas.xlsx: Análisis comparativo mensual

💡 Key Insights
- Tendencia decreciente en actividad de facturación
- Se recomienda investigar causas de la disminución
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Si tienes problemas o preguntas:

1. Revisa la documentación
2. Ejecuta los tests para verificar la instalación
3. Abre un issue en GitHub

---

**🎯 Agente Financiero v2.0** - Análisis inteligente con memoria contextual y predicciones avanzadas. 