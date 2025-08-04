# Financial Conversational Agent

Un agente conversacional inteligente para análisis financiero construido con LangGraph que interpreta preguntas en lenguaje natural, selecciona fuentes de datos relevantes y ejecuta análisis financieros cuantitativos.

## 🎯 Objetivo del Proyecto

Este proyecto valida la capacidad de construir un agente conversacional que puede:

- **Interpretar** preguntas financieras en lenguaje natural usando LLMs
- **Seleccionar** la fuente de datos más relevante entre múltiples archivos estructurados
- **Ejecutar** análisis cuantitativos correctos a partir de esos datos
- **Responder** con claridad, precisión y trazabilidad completa

## 🏗️ Arquitectura

El agente utiliza LangGraph para crear un flujo de trabajo estructurado:

```
User Question → Question Interpretation → Data Source Selection → Data Loading → Financial Analysis → Response Formatting
```

### Componentes Principales

1. **Question Interpreter**: Interpreta preguntas en lenguaje natural usando LLMs
2. **Data Selector**: Selecciona archivos Excel relevantes basado en la pregunta
3. **Data Loader**: Carga y preprocesa archivos Excel con manejo robusto de errores
4. **Financial Analyzer**: Ejecuta análisis financieros específicos
5. **Response Formatter**: Formatea respuestas con trazabilidad completa

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
pip install -r requirements.txt
```

3. **Configurar variables de entorno** (opcional):
```bash
cp .env.example .env
# Editar .env con tu API key de OpenAI
```

## 💻 Uso Básico

### Ejemplo Simple

```python
from financial_agent.agent import FinancialAgent

# Inicializar el agente
agent = FinancialAgent(api_key="tu-api-key")

# Pregunta del PRD
question = "¿Cómo variaron mis facturas por pagar y por cobrar en los últimos 2 meses?"

# Procesar la pregunta
result = agent.process_question_sync(question)

if result["success"]:
    for message in result["response"]:
        print(message.content)
else:
    print(f"Error: {result['error']}")
```

### Ejemplo Asíncrono

```python
import asyncio
from financial_agent.agent import FinancialAgent

async def main():
    agent = FinancialAgent(api_key="tu-api-key")
    
    questions = [
        "¿Cuáles son mis gastos fijos más altos?",
        "¿Cuál es el flujo de caja de los últimos 3 meses?",
        "¿Quiénes son mis clientes principales por facturación?"
    ]
    
    for question in questions:
        result = await agent.process_question(question)
        if result["success"]:
            print(f"✅ {question}")
            print(result["response"][0].content)
        else:
            print(f"❌ {question}: {result['error']}")

asyncio.run(main())
```

## 🧪 Ejecutar Tests

```bash
# Ejecutar ejemplo de uso
python financial_agent/example_usage.py

# Ejecutar tests unitarios (cuando estén disponibles)
pytest tests/
```

## 📋 Casos de Uso

### User Story Principal

> Como CEO, quiero escribir "¿Cómo variaron mis facturas por pagar y por cobrar en los últimos 2 meses?" para entender el impacto en mi flujo de caja y evaluar decisiones relacionadas con liquidez.

### Respuesta Esperada

El agente debería responder con:

1. **📊 Executive Summary (BLUF)**: Resumen ejecutivo en 1-2 oraciones
2. **📈 Detailed Analysis**: Análisis detallado con cálculos cuantitativos
3. **🔍 Data Sources Used**: Trazabilidad completa (archivo + columnas usadas)
4. **💡 Key Insights**: Recomendaciones accionables
5. **📋 Technical Details**: Datos de cálculo para verificación

## 🔧 Características Técnicas

### Robustez ante Errores

- Manejo de fechas inconsistentes
- Nombres de columnas ruidosos
- Columnas sobrantes
- Valores faltantes
- Formato de archivos inconsistente

### Análisis Financieros Soportados

- **Cash Flow**: Flujo de caja y liquidez
- **Expenses**: Análisis de gastos por categoría
- **Revenue**: Análisis de ingresos por cliente
- **Comparison**: Comparaciones entre períodos
- **Trends**: Análisis de tendencias temporales

### Trazabilidad Completa

- Mapeo de análisis a archivos fuente
- Identificación de columnas utilizadas
- Cálculos raw para verificación
- Metodologías documentadas

## 🏛️ Estructura del Proyecto

```
financial_agent/
├── __init__.py              # Inicialización del paquete
├── agent.py                 # Agente principal con LangGraph
├── state.py                 # Definiciones de estado y estructuras
├── prompts.py               # Prompts especializados
├── data_loader.py           # Carga y preprocesamiento de datos
├── financial_analyzer.py    # Análisis financiero cuantitativo
├── example_usage.py         # Ejemplos de uso
├── requirements.txt         # Dependencias
└── README.md               # Documentación
```

## 🔍 Flujo de Trabajo Detallado

1. **Interpretación de Pregunta**
   - LLM analiza la pregunta en lenguaje natural
   - Extrae tipo de análisis, período, métricas clave
   - Identifica fuentes de datos requeridas

2. **Selección de Fuentes**
   - Analiza archivos disponibles
   - Selecciona archivos relevantes
   - Identifica columnas específicas necesarias

3. **Carga de Datos**
   - Carga archivos Excel seleccionados
   - Preprocesa datos (limpieza, normalización)
   - Maneja errores de calidad de datos

4. **Análisis Financiero**
   - Ejecuta cálculos cuantitativos específicos
   - Genera insights y recomendaciones
   - Mantiene trazabilidad completa

5. **Formato de Respuesta**
   - Estructura respuesta ejecutiva
   - Incluye análisis detallado
   - Proporciona trazabilidad y detalles técnicos

## 🎯 Métricas de Éxito

- ✅ Interpretación correcta de preguntas financieras
- ✅ Selección precisa de fuentes de datos
- ✅ Cálculos cuantitativos correctos
- ✅ Respuestas con trazabilidad completa
- ✅ Manejo robusto de errores de datos
- ✅ Código modular y documentado

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Para preguntas o problemas, por favor abre un issue en el repositorio o contacta al equipo de desarrollo. 