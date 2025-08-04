#!/usr/bin/env python3
"""
Test específico para la pregunta: "Cuál es el total de facturas por cobrar emitidas en mayo?"
"""

import sys
import pandas as pd
from pathlib import Path
from typing import Dict, Any

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

def test_specific_query():
    """Probar la pregunta específica."""
    
    print("🧪 TESTING SPECIFIC QUERY")
    print("=" * 50)
    
    # Pregunta específica
    question = "Cuál es el total de facturas por cobrar emitidas en mayo?"
    print(f"❓ Pregunta: {question}")
    
    # Simular interpretación
    question_lower = question.lower()
    
    # Detectar filtros de fecha
    fecha_filtro = None
    if 'mayo' in question_lower:
        fecha_filtro = "mayo"
    
    # Determinar tipo de pregunta
    if 'total' in question_lower and 'facturas' in question_lower and 'por cobrar' in question_lower and fecha_filtro:
        question_type = "facturas_por_cobrar_total_fecha"
        data_sources = ["facturas.xlsx"]
        clarification_needed = False
    else:
        question_type = "general"
        data_sources = ["facturas.xlsx"]
        clarification_needed = True
    
    print(f"   📊 Tipo: {question_type}")
    print(f"   📁 Fuentes: {data_sources}")
    print(f"   📅 Filtro fecha: {fecha_filtro}")
    print(f"   ❓ Aclaración necesaria: {clarification_needed}")
    
    if clarification_needed:
        print("   ❌ ERROR: La pregunta debería ser interpretada correctamente")
        return
    
    # Simular carga de datos
    data_directory = Path("Datasets v2/Datasets v2")
    print(f"\n📊 Cargando datos desde: {data_directory}")
    
    try:
        # Cargar facturas
        facturas_path = data_directory / "facturas.xlsx"
        if facturas_path.exists():
            df = pd.read_excel(facturas_path)
            print(f"✅ facturas.xlsx: {len(df)} registros")
            
            # Limpiar datos
            df.columns = df.columns.str.strip().str.replace(' ', '_')
            df = df.fillna(0)
            
            # Aplicar filtro de fecha
            if fecha_filtro:
                fecha_col = None
                for col in df.columns:
                    if 'fecha' in col.lower() or 'emision' in col.lower():
                        fecha_col = col
                        break
                
                if fecha_col:
                    try:
                        df[fecha_col] = pd.to_datetime(df[fecha_col], errors='coerce')
                        df_filtrado = df[df[fecha_col].dt.month == 5]
                        print(f"📅 Registros filtrados por mayo: {len(df_filtrado)}")
                        
                        # Análisis por tipo
                        if 'Tipo' in df_filtrado.columns and 'Monto_MXN' in df_filtrado.columns:
                            facturas_por_cobrar = df_filtrado[df_filtrado['Tipo'] == 'Por cobrar']
                            total_por_cobrar = facturas_por_cobrar['Monto_MXN'].sum()
                            count_por_cobrar = len(facturas_por_cobrar)
                            
                            print(f"\n📊 RESULTADO:")
                            print(f"   💰 Total facturas por cobrar en mayo: ${total_por_cobrar:,.2f} MXN")
                            print(f"   📋 Número de facturas: {count_por_cobrar}")
                            print(f"   📅 Filtro aplicado: mayo")
                            
                            # Comparar con respuesta esperada
                            expected_total = 121000  # $121k
                            expected_count = 12
                            
                            print(f"\n🎯 COMPARACIÓN:")
                            print(f"   ✅ Tu respuesta esperada: ${expected_total:,.2f} ({expected_count} facturas)")
                            print(f"   📊 Respuesta del agente: ${total_por_cobrar:,.2f} ({count_por_cobrar} facturas)")
                            
                            if abs(total_por_cobrar - expected_total) < 1000:  # Tolerancia de $1k
                                print(f"   🎉 ¡RESULTADO CORRECTO!")
                            else:
                                print(f"   ❌ Diferencia: ${abs(total_por_cobrar - expected_total):,.2f}")
                                
                        else:
                            print("❌ No se encontraron las columnas necesarias")
                            
                    except Exception as e:
                        print(f"❌ Error aplicando filtro de fecha: {e}")
                else:
                    print("❌ No se encontró columna de fecha")
            else:
                print("❌ No se detectó filtro de fecha")
                
        else:
            print(f"❌ No se encontró el archivo: {facturas_path}")
            
    except Exception as e:
        print(f"❌ Error cargando datos: {e}")

if __name__ == "__main__":
    test_specific_query() 