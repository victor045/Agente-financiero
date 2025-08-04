"""
Sistema de Prompt Engineering para el Agente Financiero
Permite respuestas flexibles y naturales a preguntas no pre-configuradas.
"""

from typing import Dict, Any, List
import json

class FinancialPrompts:
    """Sistema de prompts para el agente financiero."""
    
    # Prompt base del sistema
    SYSTEM_PROMPT = """Eres un asistente financiero experto especializado en análisis de datos financieros.
Tu objetivo es proporcionar análisis precisos, útiles y fáciles de entender basados en datos de facturas, gastos y estado de cuenta.

CAPACIDADES:
- Analizar facturas por cobrar y por pagar
- Calcular totales, promedios, máximos y mínimos
- Filtrar por fechas, tipos y categorías
- Identificar tendencias y patrones
- Proporcionar insights financieros

ESTILO DE RESPUESTA:
- Usa lenguaje claro y profesional
- Incluye números específicos cuando sea posible
- Proporciona contexto y explicaciones
- Sé conciso pero completo
- Usa formato estructurado cuando sea apropiado

FORMATO DE DATOS:
- Montos en pesos mexicanos (MXN)
- Fechas en formato legible
- Porcentajes cuando sea relevante
- Comparaciones cuando sea útil"""

    # Prompt para análisis de datos
    ANALYSIS_PROMPT = """Analiza los siguientes datos financieros y responde la pregunta del usuario.

DATOS DISPONIBLES:
{data_summary}

PREGUNTA DEL USUARIO:
{user_question}

INSTRUCCIONES:
1. Identifica qué datos son relevantes para la pregunta
2. Realiza los cálculos necesarios
3. Proporciona una respuesta clara y específica
4. Incluye insights adicionales si son útiles
5. Si la pregunta no puede responderse con los datos disponibles, indícalo claramente

RESPUESTA:"""

    # Prompt para interpretación de preguntas
    QUESTION_INTERPRETATION_PROMPT = """Analiza la siguiente pregunta financiera y determina:
1. Qué tipo de análisis se necesita
2. Qué datos son relevantes
3. Si se requiere algún filtro específico

PREGUNTA: {question}

OPCIONES DE ANÁLISIS:
- facturas_total: Análisis general de todas las facturas
- facturas_por_cobrar: Solo facturas por cobrar
- facturas_por_pagar: Solo facturas por pagar
- facturas_por_fecha: Análisis filtrado por fecha
- facturas_por_mes: Análisis por mes
- gastos_analisis: Análisis de gastos fijos
- flujo_caja: Análisis de estado de cuenta
- comparacion: Comparación entre diferentes métricas
- tendencia: Análisis de tendencias temporales
- personalizado: Análisis específico no predefinido

RESPONDE EN FORMATO JSON:
{{
    "tipo_analisis": "tipo_identificado",
    "datos_requeridos": ["lista", "de", "datos"],
    "filtros": {{"fecha": "valor", "tipo": "valor"}},
    "especificidad": "alta|media|baja",
    "razonamiento": "explicación de por qué este análisis"
}}"""

    # Prompt para generación de respuestas
    RESPONSE_GENERATION_PROMPT = """Genera una respuesta profesional y útil para la siguiente pregunta financiera.

PREGUNTA: {question}

DATOS ANALIZADOS:
{analysis_data}

INSTRUCCIONES:
1. Proporciona una respuesta directa y específica
2. Incluye números y métricas relevantes
3. Usa formato ejecutivo cuando sea apropiado
4. Agrega insights o recomendaciones si son útiles
5. Mantén un tono profesional pero accesible

FORMATO DE RESPUESTA:
📊 Executive Summary
[Resumen ejecutivo de 1-2 líneas]

📈 Detailed Analysis
[Análisis detallado con métricas específicas]

💡 Key Insights
[Insights y recomendaciones]

🔍 Data Sources
[Fuentes de datos utilizadas]"""

    # Prompt para preguntas complejas
    COMPLEX_ANALYSIS_PROMPT = """Analiza esta pregunta financiera compleja y proporciona una respuesta integral.

PREGUNTA: {question}

DATOS DISPONIBLES:
{available_data}

INSTRUCCIONES:
1. Descompón la pregunta en partes más simples
2. Realiza múltiples análisis si es necesario
3. Combina los resultados de manera coherente
4. Proporciona una respuesta completa y bien estructurada
5. Incluye comparaciones y contexto cuando sea relevante

RESPUESTA:"""

    # Prompt para casos no pre-configurados
    FLEXIBLE_ANALYSIS_PROMPT = """Esta pregunta no está pre-configurada. Usa tu capacidad de análisis para proporcionar la mejor respuesta posible.

PREGUNTA: {question}

DATOS DISPONIBLES:
{data_summary}

INSTRUCCIONES:
1. Identifica qué aspectos de la pregunta puedes responder
2. Usa los datos disponibles de manera creativa
3. Proporciona análisis relevantes aunque no sean exactamente lo solicitado
4. Sugiere análisis alternativos si es apropiado
5. Sé transparente sobre las limitaciones

RESPUESTA:"""

    @staticmethod
    def format_data_summary(data: Dict[str, Any]) -> str:
        """Formatear resumen de datos para prompts."""
        summary = []
        
        if 'facturas' in data:
            facturas = data['facturas']
            summary.append(f"📄 FACTURAS: {len(facturas)} registros")
            if 'total' in facturas:
                summary.append(f"   - Total: ${facturas['total']:,.2f} MXN")
            if 'por_cobrar' in facturas:
                summary.append(f"   - Por cobrar: ${facturas['por_cobrar']:,.2f} MXN")
            if 'por_pagar' in facturas:
                summary.append(f"   - Por pagar: ${facturas['por_pagar']:,.2f} MXN")
        
        if 'gastos_fijos' in data:
            gastos = data['gastos_fijos']
            summary.append(f"💰 GASTOS FIJOS: {len(gastos)} registros")
            if 'total_gastos' in gastos:
                summary.append(f"   - Total: ${gastos['total_gastos']:,.2f} MXN")
        
        if 'estado_cuenta' in data:
            cuenta = data['estado_cuenta']
            summary.append(f"🏦 ESTADO DE CUENTA: {len(cuenta)} registros")
            if 'total_movimientos' in cuenta:
                summary.append(f"   - Total: ${cuenta['total_movimientos']:,.2f} MXN")
        
        return "\n".join(summary)

    @staticmethod
    def create_analysis_prompt(question: str, data: Dict[str, Any]) -> str:
        """Crear prompt para análisis de datos."""
        data_summary = FinancialPrompts.format_data_summary(data)
        return FinancialPrompts.ANALYSIS_PROMPT.format(
            data_summary=data_summary,
            user_question=question
        )

    @staticmethod
    def create_interpretation_prompt(question: str) -> str:
        """Crear prompt para interpretación de preguntas."""
        return FinancialPrompts.QUESTION_INTERPRETATION_PROMPT.format(
            question=question
        )

    @staticmethod
    def create_response_prompt(question: str, analysis_data: Dict[str, Any]) -> str:
        """Crear prompt para generación de respuestas."""
        return FinancialPrompts.RESPONSE_GENERATION_PROMPT.format(
            question=question,
            analysis_data=json.dumps(analysis_data, indent=2, default=str)
        )

    @staticmethod
    def create_complex_analysis_prompt(question: str, data: Dict[str, Any]) -> str:
        """Crear prompt para análisis complejo."""
        data_summary = FinancialPrompts.format_data_summary(data)
        return FinancialPrompts.COMPLEX_ANALYSIS_PROMPT.format(
            question=question,
            available_data=data_summary
        )

    @staticmethod
    def create_flexible_analysis_prompt(question: str, data: Dict[str, Any]) -> str:
        """Crear prompt para casos no pre-configurados."""
        data_summary = FinancialPrompts.format_data_summary(data)
        return FinancialPrompts.FLEXIBLE_ANALYSIS_PROMPT.format(
            question=question,
            data_summary=data_summary
        )


class PromptManager:
    """Gestor de prompts para el agente financiero."""
    
    def __init__(self):
        self.prompts = FinancialPrompts()
        self.conversation_history = []
    
    def add_to_history(self, role: str, content: str):
        """Agregar mensaje al historial de conversación."""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": "now"  # En implementación real usar datetime
        })
    
    def get_context_prompt(self, question: str, data: Dict[str, Any]) -> str:
        """Obtener prompt con contexto de conversación."""
        context = ""
        if self.conversation_history:
            context = "\n\nCONTEXTO DE CONVERSACIÓN PREVIA:\n"
            for msg in self.conversation_history[-3:]:  # Últimos 3 mensajes
                context += f"{msg['role'].upper()}: {msg['content']}\n"
        
        return f"{FinancialPrompts.SYSTEM_PROMPT}\n{context}\n{self.prompts.create_analysis_prompt(question, data)}"
    
    def clear_history(self):
        """Limpiar historial de conversación."""
        self.conversation_history = []


# Funciones de utilidad para prompts
def create_simple_prompt(question: str, data: Dict[str, Any]) -> str:
    """Crear prompt simple para análisis básico."""
    return f"""
Analiza estos datos financieros y responde: {question}

DATOS:
{FinancialPrompts.format_data_summary(data)}

RESPUESTA:"""


def create_comparison_prompt(question: str, data: Dict[str, Any]) -> str:
    """Crear prompt para análisis comparativo."""
    return f"""
Realiza un análisis comparativo para: {question}

DATOS DISPONIBLES:
{FinancialPrompts.format_data_summary(data)}

INSTRUCCIONES:
1. Identifica los elementos a comparar
2. Calcula las diferencias y similitudes
3. Proporciona insights sobre las comparaciones
4. Sugiere conclusiones relevantes

ANÁLISIS:"""


def create_trend_analysis_prompt(question: str, data: Dict[str, Any]) -> str:
    """Crear prompt para análisis de tendencias."""
    return f"""
Analiza las tendencias para: {question}

DATOS DISPONIBLES:
{FinancialPrompts.format_data_summary(data)}

INSTRUCCIONES:
1. Identifica patrones temporales
2. Calcula tasas de crecimiento/decrecimiento
3. Identifica picos y valles
4. Proyecta tendencias futuras si es posible
5. Proporciona recomendaciones basadas en tendencias

ANÁLISIS DE TENDENCIAS:""" 