#!/usr/bin/env python3
"""
Script de diagnóstico para verificar los datos exactos que se están procesando.
"""
import sys
import os
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from enhanced_financial_agent_with_llm import FinancialAgentConfig, FinancialDataProcessor

def diagnosticar_datos():
    print("🔍 DIAGNÓSTICO DE DATOS")
    print("=" * 60)
    
    config = FinancialAgentConfig()
    processor = FinancialDataProcessor(config)
    
    # Cargar datos
    print("📊 Cargando datos...")
    data = processor.load_all_data()
    
    if 'facturas' in data:
        df = data['facturas']
        print(f"\n📋 DATOS DE FACTURAS:")
        print(f"Total de registros: {len(df)}")
        print(f"Columnas disponibles: {list(df.columns)}")
        
        # Mostrar primeras filas
        print(f"\n📄 Primeras 5 filas:")
        print(df.head())
        
        # Análisis de fechas
        fecha_col = None
        for col in df.columns:
            if 'fecha' in col.lower() or 'emision' in col.lower():
                fecha_col = col
                break
        
        if fecha_col:
            print(f"\n📅 Análisis de fechas (columna: {fecha_col}):")
            df[fecha_col] = pd.to_datetime(df[fecha_col], errors='coerce')
            df['mes'] = df[fecha_col].dt.month
            df['mes_nombre'] = df[fecha_col].dt.month_name()
            
            # Análisis por mes
            monthly_stats = df.groupby(['mes', 'mes_nombre']).size().reset_index(name='count')
            print(f"\n📊 Facturas por mes:")
            for _, row in monthly_stats.iterrows():
                print(f"  - {row['mes_nombre']}: {row['count']} facturas")
            
            # Análisis de mayo específicamente
            mayo_data = df[df['mes'] == 5]  # Mayo es mes 5
            print(f"\n🌺 ANÁLISIS ESPECÍFICO DE MAYO:")
            print(f"Facturas en mayo: {len(mayo_data)}")
            
            if len(mayo_data) > 0:
                # Encontrar columna de monto
                amount_col = None
                for col in mayo_data.columns:
                    if 'monto' in col.lower() or 'amount' in col.lower():
                        amount_col = col
                        break
                
                if amount_col:
                    total_mayo = mayo_data[amount_col].sum()
                    print(f"Monto total en mayo: ${total_mayo:,.2f} MXN")
                    print(f"Promedio por factura: ${total_mayo/len(mayo_data):,.2f} MXN")
                    
                    print(f"\n📋 Detalle de facturas en mayo:")
                    for idx, row in mayo_data.iterrows():
                        print(f"  - Factura {idx}: ${row[amount_col]:,.2f} MXN")
                else:
                    print("❌ No se encontró columna de monto")
            else:
                print("❌ No se encontraron facturas en mayo")
        
        # Análisis por tipo
        if 'Tipo' in df.columns:
            print(f"\n📊 Análisis por tipo:")
            tipo_counts = df['Tipo'].value_counts()
            for tipo, count in tipo_counts.items():
                print(f"  - {tipo}: {count} facturas")
        
        # Análisis completo de montos
        amount_col = processor._get_amount_column(df)
        if amount_col:
            print(f"\n💰 ANÁLISIS DE MONTOS:")
            print(f"Columna de monto: {amount_col}")
            print(f"Total general: ${df[amount_col].sum():,.2f} MXN")
            print(f"Promedio general: ${df[amount_col].mean():,.2f} MXN")
            print(f"Factura más alta: ${df[amount_col].max():,.2f} MXN")
            print(f"Factura más baja: ${df[amount_col].min():,.2f} MXN")
            
            # Análisis mensual de montos
            if fecha_col:
                monthly_amounts = df.groupby(['mes', 'mes_nombre'])[amount_col].agg(['sum', 'count', 'mean']).reset_index()
                print(f"\n📈 MONTOS POR MES:")
                for _, row in monthly_amounts.iterrows():
                    print(f"  - {row['mes_nombre']}: {row['count']} facturas, ${row['sum']:,.2f} MXN total")
    
    else:
        print("❌ No se encontraron datos de facturas")

if __name__ == "__main__":
    diagnosticar_datos() 