"""
Demo script para probar el Financial Agent con datos reales.
Ejecuta este script para ver el agente en acción.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def demo_data_analysis():
    """Demo del análisis de datos reales."""
    print("🚀 DEMO: Financial Agent - Análisis de Datos Reales")
    print("=" * 60)
    
    # Cargar datos reales
    data_directory = Path("Datasets v2/Datasets v2")
    
    if not data_directory.exists():
        print("❌ Error: No se encontró el directorio de datos")
        print("Asegúrate de que los archivos Excel estén en: Datasets v2/Datasets v2/")
        return
    
    print("📊 Cargando datos reales...")
    
    # Cargar facturas
    facturas_path = data_directory / "facturas.xlsx"
    if facturas_path.exists():
        facturas_df = pd.read_excel(facturas_path)
        print(f"✅ facturas.xlsx cargado: {len(facturas_df)} facturas")
        
        # Análisis básico
        if 'Monto (MXN)' in facturas_df.columns:
            total = facturas_df['Monto (MXN)'].sum()
            print(f"   💰 Total facturas: ${total:,.2f} MXN")
            
            if 'Tipo' in facturas_df.columns:
                por_cobrar = facturas_df[facturas_df['Tipo'] == 'Por cobrar']['Monto (MXN)'].sum()
                por_pagar = facturas_df[facturas_df['Tipo'] == 'Por pagar']['Monto (MXN)'].sum()
                print(f"   📈 Por cobrar: ${por_cobrar:,.2f} MXN")
                print(f"   📉 Por pagar: ${por_pagar:,.2f} MXN")
    else:
        print("❌ facturas.xlsx no encontrado")
    
    # Cargar gastos fijos
    gastos_path = data_directory / "gastos_fijos.xlsx"
    if gastos_path.exists():
        gastos_df = pd.read_excel(gastos_path)
        print(f"✅ gastos_fijos.xlsx cargado: {len(gastos_df)} gastos")
        
        if 'Monto (MXN)' in gastos_df.columns:
            total_gastos = gastos_df['Monto (MXN)'].sum()
            print(f"   💰 Total gastos fijos: ${total_gastos:,.2f} MXN")
            
            if 'Gasto Fijo' in gastos_df.columns:
                print("   📋 Categorías de gastos:")
                for _, row in gastos_df.iterrows():
                    print(f"      - {row['Gasto Fijo']}: ${row['Monto (MXN)']:,.2f}")
    else:
        print("❌ gastos_fijos.xlsx no encontrado")
    
    # Cargar estado de cuenta
    estado_path = data_directory / "Estado_cuenta.xlsx"
    if estado_path.exists():
        estado_df = pd.read_excel(estado_path)
        print(f"✅ Estado_cuenta.xlsx cargado: {len(estado_df)} movimientos")
        
        if 'Monto de la transacción (MXN)' in estado_df.columns:
            ingresos = estado_df[estado_df['Monto de la transacción (MXN)'] > 0]['Monto de la transacción (MXN)'].sum()
            egresos = estado_df[estado_df['Monto de la transacción (MXN)'] < 0]['Monto de la transacción (MXN)'].sum()
            neto = ingresos + egresos
            
            print(f"   💰 Ingresos: ${ingresos:,.2f} MXN")
            print(f"   💸 Egresos: ${abs(egresos):,.2f} MXN")
            print(f"   📊 Flujo neto: ${neto:,.2f} MXN")
    else:
        print("❌ Estado_cuenta.xlsx no encontrado")


def demo_questions():
    """Demo de preguntas que el agente puede responder."""
    print("\n" + "=" * 60)
    print("❓ PREGUNTAS QUE EL AGENTE PUEDE RESPONDER")
    print("=" * 60)
    
    questions = [
        "¿Cuál es el total de facturas emitidas?",
        "¿Cuál es el promedio de las facturas?",
        "¿Cuáles son mis clientes principales?",
        "¿Cómo se distribuyen las facturas por tipo (por cobrar vs por pagar)?",
        "¿Cuáles son mis gastos fijos más altos?",
        "¿Cuál es el total de gastos fijos?",
        "¿Cómo se distribuyen mis gastos por categoría?",
        "¿Cuál es mi flujo de caja?",
        "¿Cuáles son mis ingresos y egresos?",
        "¿Cuál es el saldo de mi cuenta bancaria?",
        "¿Cómo variaron mis facturas por pagar y por cobrar en los últimos 2 meses?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"{i:2d}. {question}")
    
    print(f"\n💡 El agente puede responder a estas y muchas más preguntas!")
    print("   Solo necesitas hacer la pregunta en lenguaje natural.")


def demo_response_format():
    """Demo del formato de respuesta del agente."""
    print("\n" + "=" * 60)
    print("📋 FORMATO DE RESPUESTA DEL AGENTE")
    print("=" * 60)
    
    print("""
📊 Executive Summary
[Resumen ejecutivo en formato BLUF - Bottom Line Up Front]

📈 Detailed Analysis
[Análisis detallado con cálculos y métricas]

🔍 Data Sources Used
[Fuentes de datos utilizadas con trazabilidad completa]

💡 Key Insights & Recommendations
[Insights clave y recomendaciones para la toma de decisiones]

📋 Technical Details
[Detalles técnicos y metodología para verificación]
    """)


def demo_installation():
    """Instrucciones de instalación."""
    print("\n" + "=" * 60)
    print("🔧 INSTRUCCIONES DE INSTALACIÓN")
    print("=" * 60)
    
    print("""
1. INSTALAR DEPENDENCIAS:
   pip3 install pandas numpy openpyxl

2. VERIFICAR DATOS:
   - Los archivos Excel deben estar en: Datasets v2/Datasets v2/
   - facturas.xlsx
   - gastos_fijos.xlsx  
   - Estado_cuenta.xlsx

3. EJECUTAR TESTS:
   python3 financial_agent/final_data_test.py

4. EJECUTAR DEMO COMPLETO:
   python3 financial_agent/run_demo.py
    """)


def main():
    """Función principal del demo."""
    print("🎯 FINANCIAL AGENT - DEMO")
    print("=" * 60)
    
    try:
        # Demo de análisis de datos
        demo_data_analysis()
        
        # Demo de preguntas
        demo_questions()
        
        # Demo de formato de respuesta
        demo_response_format()
        
        # Instrucciones de instalación
        demo_installation()
        
        print("\n" + "=" * 60)
        print("✅ DEMO COMPLETADO")
        print("=" * 60)
        print("🎉 El Financial Agent está listo para usar!")
        print("📚 Revisa la documentación en README.md para más detalles")
        
    except Exception as e:
        print(f"❌ Error en el demo: {e}")
        print("💡 Asegúrate de tener las dependencias instaladas y los datos en su lugar")


if __name__ == "__main__":
    main() 