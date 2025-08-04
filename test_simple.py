#!/usr/bin/env python3
"""
Test simple y directo del intérprete de preguntas.
"""

# Importar solo lo necesario para el test
from typing import Dict, Any

class QuestionInterpreter:
    """Intérprete de preguntas financieras con aclaraciones."""
    
    @staticmethod
    def interpret_question(question: str) -> Dict[str, Any]:
        """Interpretar la pregunta del usuario."""
        question_lower = question.lower()
        
        # Detectar filtros de fecha
        fecha_filtro = None
        if 'mayo' in question_lower:
            fecha_filtro = "mayo"
        elif 'junio' in question_lower:
            fecha_filtro = "junio"
        elif 'julio' in question_lower:
            fecha_filtro = "julio"
        elif 'agosto' in question_lower:
            fecha_filtro = "agosto"
        elif 'septiembre' in question_lower:
            fecha_filtro = "septiembre"
        elif 'octubre' in question_lower:
            fecha_filtro = "octubre"
        elif 'noviembre' in question_lower:
            fecha_filtro = "noviembre"
        elif 'diciembre' in question_lower:
            fecha_filtro = "diciembre"
        elif 'enero' in question_lower:
            fecha_filtro = "enero"
        elif 'febrero' in question_lower:
            fecha_filtro = "febrero"
        elif 'marzo' in question_lower:
            fecha_filtro = "marzo"
        elif 'abril' in question_lower:
            fecha_filtro = "abril"
        
        # Determinar tipo de pregunta con filtros específicos
        if 'por pagar' in question_lower and 'alta' in question_lower:
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
            question_type = "general"
            data_sources = ["facturas.xlsx", "gastos_fijos.xlsx", "Estado_cuenta.xlsx"]
            clarification_needed = False
        
        return {
            "question_type": question_type,
            "data_sources": data_sources,
            "fecha_filtro": fecha_filtro,
            "analysis_required": f"Análisis de {question_type}",
            "clarification_needed": clarification_needed,
            "clarification_question": ""
        }

def test_question_interpreter():
    """Probar el intérprete de preguntas."""
    
    test_questions = [
        "Cuál es el total de facturas por cobrar emitidas en mayo?",
        "¿Cuál es la factura por pagar más alta?",
        "¿Cuál es el total de facturas emitidas?",
        "¿Cuál es el promedio de facturas por cobrar?",
        "¿Cuáles son los gastos fijos más altos?",
        "¿Cómo está el flujo de caja?"
    ]
    
    print("🧪 TESTING QUESTION INTERPRETER")
    print("=" * 50)
    
    for question in test_questions:
        print(f"\n❓ Pregunta: {question}")
        interpretation = QuestionInterpreter.interpret_question(question)
        
        print(f"   📊 Tipo: {interpretation['question_type']}")
        print(f"   📁 Fuentes: {interpretation['data_sources']}")
        if interpretation.get('fecha_filtro'):
            print(f"   📅 Filtro fecha: {interpretation['fecha_filtro']}")
        print(f"   ❓ Aclaración necesaria: {interpretation['clarification_needed']}")

if __name__ == "__main__":
    test_question_interpreter() 