"""
Interactive Financial Agent con Visualización de Progreso en Tiempo Real.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import time
import sys
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InteractiveFinancialAgentWithProgress:
    """Agente financiero interactivo con visualización de progreso."""
    
    def __init__(self):
        self.data_directory = Path("Datasets v2/Datasets v2")
        self.data = {}
        self.last_analysis = {}
        self.current_step = None
        self.load_data()
    
    def load_data(self):
        """Cargar todos los datos de Excel."""
        print("📊 Cargando datos financieros...")
        
        # Cargar facturas
        facturas_path = self.data_directory / "facturas.xlsx"
        if facturas_path.exists():
            self.data['facturas'] = pd.read_excel(facturas_path)
            print(f"✅ facturas.xlsx: {len(self.data['facturas'])} facturas")
        
        # Cargar gastos fijos
        gastos_path = self.data_directory / "gastos_fijos.xlsx"
        if gastos_path.exists():
            self.data['gastos_fijos'] = pd.read_excel(gastos_path)
            print(f"✅ gastos_fijos.xlsx: {len(self.data['gastos_fijos'])} gastos")
        
        # Cargar estado de cuenta
        estado_path = self.data_directory / "Estado_cuenta.xlsx"
        if estado_path.exists():
            self.data['Estado_cuenta'] = pd.read_excel(estado_path)
            print(f"✅ Estado_cuenta.xlsx: {len(self.data['Estado_cuenta'])} movimientos")
    
    def show_progress(self, step_name, description=""):
        """Mostrar progreso del paso actual."""
        self.current_step = step_name
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        print(f"\n🔄 [{timestamp}] PASO: {step_name}")
        if description:
            print(f"   📝 {description}")
        
        # Mostrar visualización del grafo con paso actual
        self.visualize_current_step()
    
    def visualize_current_step(self):
        """Visualizar el paso actual en el grafo."""
        steps = {
            "interpret_question": "🔵 Interpretar Pregunta",
            "select_data_sources": "🟢 Seleccionar Fuentes",
            "load_and_analyze": "🔴 Cargar y Analizar", 
            "format_response": "🟡 Formatear Respuesta",
            "END": "⚫ FIN"
        }
        
        print("\n📊 ESTADO ACTUAL DEL GRAFO:")
        print("=" * 50)
        
        for step, label in steps.items():
            if step == self.current_step:
                print(f"   ▶️  {label} [ACTUAL]")
            elif step in ["interpret_question", "select_data_sources", "load_and_analyze", "format_response"]:
                if self.is_step_completed(step):
                    print(f"   ✅ {label} [COMPLETADO]")
                else:
                    print(f"   ⏳ {label} [PENDIENTE]")
            else:
                print(f"   ⏳ {label} [PENDIENTE]")
        
        print("=" * 50)
    
    def is_step_completed(self, step):
        """Verificar si un paso está completado."""
        completed_steps = []
        
        if hasattr(self, 'question_interpreted'):
            completed_steps.append("interpret_question")
        if hasattr(self, 'data_selected'):
            completed_steps.append("select_data_sources")
        if hasattr(self, 'analysis_completed'):
            completed_steps.append("load_and_analyze")
        if hasattr(self, 'response_formatted'):
            completed_steps.append("format_response")
        
        return step in completed_steps
    
    def analyze_facturas(self):
        """Analizar datos de facturas."""
        if 'facturas' not in self.data:
            return {}
        
        df = self.data['facturas']
        analysis = {}
        
        if 'Monto (MXN)' in df.columns:
            analysis['total'] = df['Monto (MXN)'].sum()
            analysis['promedio'] = df['Monto (MXN)'].mean()
            analysis['min'] = df['Monto (MXN)'].min()
            analysis['max'] = df['Monto (MXN)'].max()
            analysis['count'] = len(df)
        
        if 'Tipo' in df.columns and 'Monto (MXN)' in df.columns:
            # Análisis por tipo
            por_cobrar = df[df['Tipo'] == 'Por cobrar']['Monto (MXN)'].sum()
            por_pagar = df[df['Tipo'] == 'Por pagar']['Monto (MXN)'].sum()
            analysis['por_cobrar'] = por_cobrar
            analysis['por_pagar'] = por_pagar
            
            # Análisis detallado por tipo
            facturas_por_cobrar = df[df['Tipo'] == 'Por cobrar']
            facturas_por_pagar = df[df['Tipo'] == 'Por pagar']
            
            if not facturas_por_cobrar.empty:
                analysis['por_cobrar_max'] = facturas_por_cobrar['Monto (MXN)'].max()
                analysis['por_cobrar_min'] = facturas_por_cobrar['Monto (MXN)'].min()
                analysis['por_cobrar_count'] = len(facturas_por_cobrar)
                analysis['por_cobrar_promedio'] = facturas_por_cobrar['Monto (MXN)'].mean()
            
            if not facturas_por_pagar.empty:
                analysis['por_pagar_max'] = facturas_por_pagar['Monto (MXN)'].max()
                analysis['por_pagar_min'] = facturas_por_pagar['Monto (MXN)'].min()
                analysis['por_pagar_count'] = len(facturas_por_pagar)
                analysis['por_pagar_promedio'] = facturas_por_pagar['Monto (MXN)'].mean()
        
        return analysis
    
    def process_question_with_progress(self, question):
        """Procesar pregunta mostrando progreso en tiempo real."""
        print(f"\n🎯 PROCESANDO PREGUNTA: {question}")
        print("=" * 60)
        
        # Paso 1: Interpretar pregunta
        self.show_progress("interpret_question", "Analizando la pregunta del usuario...")
        time.sleep(1)  # Simular procesamiento
        
        # Simular interpretación
        question_lower = question.lower()
        if 'por pagar' in question_lower and 'alta' in question_lower:
            question_type = "facturas_por_pagar_max"
        elif 'por cobrar' in question_lower and 'alta' in question_lower:
            question_type = "facturas_por_cobrar_max"
        elif 'total' in question_lower:
            question_type = "facturas_total"
        else:
            question_type = "general"
        
        self.question_interpreted = True
        print(f"   ✅ Interpretación completada: {question_type}")
        
        # Paso 2: Seleccionar fuentes de datos
        self.show_progress("select_data_sources", "Seleccionando archivos Excel relevantes...")
        time.sleep(1)
        
        selected_files = []
        if 'facturas' in question_lower:
            selected_files.append('facturas.xlsx')
        if 'gastos' in question_lower:
            selected_files.append('gastos_fijos.xlsx')
        if 'cuenta' in question_lower or 'flujo' in question_lower:
            selected_files.append('Estado_cuenta.xlsx')
        
        if not selected_files:
            selected_files = ['facturas.xlsx']  # Default
        
        self.data_selected = True
        print(f"   ✅ Fuentes seleccionadas: {', '.join(selected_files)}")
        
        # Paso 3: Cargar y analizar
        self.show_progress("load_and_analyze", "Cargando datos y realizando análisis...")
        time.sleep(1.5)
        
        analysis = self.analyze_facturas()
        self.analysis_completed = True
        print(f"   ✅ Análisis completado: {len(analysis)} métricas calculadas")
        
        # Paso 4: Formatear respuesta
        self.show_progress("format_response", "Formateando respuesta ejecutiva...")
        time.sleep(1)
        
        response = self.format_response(question, analysis, question_type)
        self.response_formatted = True
        
        # Paso 5: Finalizar
        self.show_progress("END", "Proceso completado")
        time.sleep(0.5)
        
        return response
    
    def format_response(self, question, analysis, question_type):
        """Formatear respuesta basada en el tipo de pregunta."""
        if question_type == "facturas_por_pagar_max" and 'por_pagar_max' in analysis:
            return f"""
📊 Executive Summary
La factura por pagar más alta es: ${analysis['por_pagar_max']:,.2f} MXN

📈 Detailed Analysis
- Factura por pagar más alta: ${analysis['por_pagar_max']:,.2f} MXN
- Total facturas por pagar: {analysis['por_pagar_count']}
- Promedio facturas por pagar: ${analysis['por_pagar_promedio']:,.2f} MXN
- Total por pagar: ${analysis['por_pagar']:,.2f} MXN

🔍 Data Sources Used
- facturas.xlsx: Tipo, Monto (MXN) - Filtrado por "Por pagar"

💡 Key Insights
- La factura por pagar más alta representa ${(analysis['por_pagar_max']/analysis['por_pagar']*100):.1f}% del total por pagar
- Cantidad específica: ${analysis['por_pagar_max']:,.2f} pesos mexicanos
"""
        
        elif question_type == "facturas_por_cobrar_max" and 'por_cobrar_max' in analysis:
            return f"""
📊 Executive Summary
La factura por cobrar más alta es: ${analysis['por_cobrar_max']:,.2f} MXN

📈 Detailed Analysis
- Factura por cobrar más alta: ${analysis['por_cobrar_max']:,.2f} MXN
- Total facturas por cobrar: {analysis['por_cobrar_count']}
- Promedio facturas por cobrar: ${analysis['por_cobrar_promedio']:,.2f} MXN
- Total por cobrar: ${analysis['por_cobrar']:,.2f} MXN

🔍 Data Sources Used
- facturas.xlsx: Tipo, Monto (MXN) - Filtrado por "Por cobrar"

💡 Key Insights
- La factura por cobrar más alta representa ${(analysis['por_cobrar_max']/analysis['por_cobrar']*100):.1f}% del total por cobrar
- Cantidad específica: ${analysis['por_cobrar_max']:,.2f} pesos mexicanos
"""
        
        elif question_type == "facturas_total":
            return f"""
📊 Executive Summary
Total de facturas emitidas: ${analysis['total']:,.2f} MXN

📈 Detailed Analysis
- Total facturas: ${analysis['total']:,.2f} MXN
- Número de facturas: {analysis['count']}
- Promedio por factura: ${analysis['promedio']:,.2f} MXN
- Factura más alta: ${analysis['max']:,.2f} MXN
- Factura más baja: ${analysis['min']:,.2f} MXN

🔍 Data Sources Used
- facturas.xlsx: Folio de Factura, Tipo, Cliente/Proveedor, Fecha de Emisión, Monto (MXN)

💡 Key Insights
- Total de ingresos por facturas: ${analysis['total']:,.2f} MXN
- Promedio de factura: ${analysis['promedio']:,.2f} MXN
- Cantidad específica: ${analysis['total']:,.2f} pesos mexicanos
"""
        
        else:
            return f"""
📊 Executive Summary
Análisis general de facturas

📈 Detailed Analysis
- Total facturas: ${analysis['total']:,.2f} MXN
- Por cobrar: ${analysis.get('por_cobrar', 0):,.2f} MXN
- Por pagar: ${analysis.get('por_pagar', 0):,.2f} MXN

🔍 Data Sources Used
- facturas.xlsx: Datos completos de facturas

💡 Key Insights
- Análisis completado para la pregunta: "{question}"
- Cantidades específicas disponibles en el análisis detallado
"""
    
    def show_completion_summary(self):
        """Mostrar resumen de completación."""
        print("\n🎉 RESUMEN DE EJECUCIÓN")
        print("=" * 50)
        
        steps = [
            ("interpret_question", "Interpretación de pregunta"),
            ("select_data_sources", "Selección de fuentes"),
            ("load_and_analyze", "Análisis de datos"),
            ("format_response", "Formateo de respuesta")
        ]
        
        for step, description in steps:
            if self.is_step_completed(step):
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description}")
        
        print("=" * 50)


def main():
    """Función principal del agente interactivo con progreso."""
    print("🎯 FINANCIAL AGENT - INTERACTIVO CON PROGRESO")
    print("=" * 60)
    print("💡 Haz preguntas sobre tus datos financieros")
    print("📊 Ejemplos de preguntas:")
    print("   - ¿Cuál es el total de facturas emitidas?")
    print("   - ¿Cuáles son mis gastos fijos más altos?")
    print("   - ¿Cuál es mi flujo de caja?")
    print("   - ¿Cómo se distribuyen las facturas por tipo?")
    print("   - ¿Cuál es el saldo de mi cuenta bancaria?")
    print("   - ¿Cuál es la factura por pagar más alta?")
    print("   - ¿Cuál es la factura por cobrar más alta?")
    print("   - ¿Cómo variaron mis facturas por pagar y por cobrar?")
    print("=" * 60)
    
    agent = InteractiveFinancialAgentWithProgress()
    
    while True:
        try:
            question = input("\n❓ Tu pregunta (o 'salir' para terminar): ").strip()
            
            if question.lower() in ['salir', 'exit', 'quit', 'q']:
                print("👋 ¡Hasta luego!")
                break
            
            if not question:
                continue
            
            # Procesar pregunta con progreso
            response = agent.process_question_with_progress(question)
            
            # Mostrar respuesta
            print("\n" + "=" * 60)
            print("📋 RESPUESTA:")
            print("=" * 60)
            print(response)
            
            # Mostrar resumen de completación
            agent.show_completion_summary()
            
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Intenta con otra pregunta")


if __name__ == "__main__":
    main() 