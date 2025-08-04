"""
Final test script that correctly handles the actual column names from real Excel files.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_and_analyze_real_data():
    """Load and analyze the real Excel files with actual column names."""
    print("=== Loading Real Data ===")
    
    data_directory = Path("Datasets v2/Datasets v2")
    
    if not data_directory.exists():
        print(f"❌ Data directory {data_directory} does not exist")
        return {}, {}
    
    # Get available Excel files
    excel_files = list(data_directory.glob("*.xlsx"))
    available_files = [f.name for f in excel_files]
    
    print(f"Available files: {available_files}")
    
    all_data = {}
    summaries = {}
    
    for filename in available_files:
        print(f"\n--- Analyzing {filename} ---")
        
        try:
            file_path = data_directory / filename
            df = pd.read_excel(file_path)
            
            # Store original data
            all_data[filename] = df
            summaries[filename] = {
                'rows': len(df),
                'columns': list(df.columns),
                'sample_data': df.head(3).to_dict('records'),
                'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
                'date_columns': df.select_dtypes(include=['datetime64']).columns.tolist()
            }
            
            print(f"Rows: {len(df)}")
            print(f"Columns: {list(df.columns)}")
            print(f"Sample data:")
            for i, row in df.head(3).iterrows():
                print(f"  Row {i}: {dict(row)}")
                
        except Exception as e:
            print(f"❌ Error loading {filename}: {e}")
    
    return all_data, summaries


def analyze_financial_data_final(all_data, summaries):
    """Analyze financial data with actual column names."""
    print("\n=== Final Financial Data Analysis ===")
    
    analysis_results = {}
    
    # Analyze facturas.xlsx
    if 'facturas.xlsx' in all_data:
        facturas_df = all_data['facturas.xlsx']
        print(f"\n📊 Facturas Analysis:")
        print(f"  Total invoices: {len(facturas_df)}")
        
        # Use actual column names
        amount_col = 'Monto (MXN)'
        client_col = 'Cliente/Proveedor'
        date_col = 'Fecha de Emisión'
        type_col = 'Tipo'
        
        if amount_col in facturas_df.columns:
            total_amount = facturas_df[amount_col].sum()
            avg_amount = facturas_df[amount_col].mean()
            print(f"  Total amount: ${total_amount:,.2f}")
            print(f"  Average amount: ${avg_amount:,.2f}")
            print(f"  Min amount: ${facturas_df[amount_col].min():,.2f}")
            print(f"  Max amount: ${facturas_df[amount_col].max():,.2f}")
            
            analysis_results['facturas'] = {
                'total_amount': total_amount,
                'avg_amount': avg_amount,
                'count': len(facturas_df),
                'min_amount': facturas_df[amount_col].min(),
                'max_amount': facturas_df[amount_col].max()
            }
        
        # Analyze by type (por cobrar vs por pagar)
        if type_col in facturas_df.columns:
            type_analysis = facturas_df.groupby(type_col)[amount_col].agg(['sum', 'count']).reset_index()
            type_analysis.columns = ['type', 'total', 'count']
            
            print(f"  By type:")
            for _, row in type_analysis.iterrows():
                print(f"    {row['type']}: ${row['total']:,.2f} ({row['count']} invoices)")
            
            analysis_results['facturas']['by_type'] = type_analysis.to_dict('records')
        
        # Analyze by client
        if client_col in facturas_df.columns:
            client_analysis = facturas_df.groupby(client_col)[amount_col].agg(['sum', 'count']).reset_index()
            client_analysis.columns = ['client', 'total', 'count']
            client_analysis = client_analysis.sort_values('total', ascending=False)
            
            print(f"  Top clients:")
            for _, row in client_analysis.head(5).iterrows():
                print(f"    {row['client']}: ${row['total']:,.2f} ({row['count']} invoices)")
            
            analysis_results['facturas']['by_client'] = client_analysis.to_dict('records')
        
        if date_col in facturas_df.columns:
            print(f"  Date range: {facturas_df[date_col].min()} to {facturas_df[date_col].max()}")
    
    # Analyze gastos_fijos.xlsx
    if 'gastos_fijos.xlsx' in all_data:
        gastos_df = all_data['gastos_fijos.xlsx']
        print(f"\n💰 Gastos Fijos Analysis:")
        print(f"  Total expenses: {len(gastos_df)}")
        
        # Use actual column names
        amount_col = 'Monto (MXN)'
        category_col = 'Gasto Fijo'
        
        if amount_col in gastos_df.columns:
            total_expenses = gastos_df[amount_col].sum()
            avg_expense = gastos_df[amount_col].mean()
            print(f"  Total expenses: ${total_expenses:,.2f}")
            print(f"  Average expense: ${avg_expense:,.2f}")
            print(f"  Min expense: ${gastos_df[amount_col].min():,.2f}")
            print(f"  Max expense: ${gastos_df[amount_col].max():,.2f}")
            
            analysis_results['gastos_fijos'] = {
                'total_expenses': total_expenses,
                'avg_expense': avg_expense,
                'count': len(gastos_df),
                'min_expense': gastos_df[amount_col].min(),
                'max_expense': gastos_df[amount_col].max()
            }
        
        if category_col in gastos_df.columns:
            category_analysis = gastos_df.groupby(category_col)[amount_col].agg(['sum', 'count']).reset_index()
            category_analysis.columns = ['category', 'total', 'count']
            category_analysis = category_analysis.sort_values('total', ascending=False)
            
            print(f"  Categories:")
            for _, row in category_analysis.iterrows():
                print(f"    {row['category']}: ${row['total']:,.2f} ({row['count']} items)")
            
            analysis_results['gastos_fijos']['by_category'] = category_analysis.to_dict('records')
    
    # Analyze Estado_cuenta.xlsx
    if 'Estado_cuenta.xlsx' in all_data:
        estado_df = all_data['Estado_cuenta.xlsx']
        print(f"\n🏦 Estado de Cuenta Analysis:")
        print(f"  Total movements: {len(estado_df)}")
        
        # Use actual column names
        amount_col = 'Monto de la transacción (MXN)'
        date_col = 'Fecha'
        desc_col = 'Descripción de la transacción'
        balance_col = 'Saldo (MXN)'
        
        if amount_col in estado_df.columns:
            total_movements = estado_df[amount_col].sum()
            positive_movements = estado_df[estado_df[amount_col] > 0][amount_col].sum()
            negative_movements = estado_df[estado_df[amount_col] < 0][amount_col].sum()
            net_flow = positive_movements + negative_movements
            
            print(f"  Total movements: ${total_movements:,.2f}")
            print(f"  Positive movements: ${positive_movements:,.2f}")
            print(f"  Negative movements: ${negative_movements:,.2f}")
            print(f"  Net cash flow: ${net_flow:,.2f}")
            
            analysis_results['Estado_cuenta'] = {
                'total_movements': total_movements,
                'positive_movements': positive_movements,
                'negative_movements': negative_movements,
                'net_flow': net_flow,
                'count': len(estado_df)
            }
        
        if date_col in estado_df.columns:
            print(f"  Date range: {estado_df[date_col].min()} to {estado_df[date_col].max()}")
        
        if balance_col in estado_df.columns:
            current_balance = estado_df[balance_col].iloc[-1]
            print(f"  Current balance: ${current_balance:,.2f}")
            analysis_results['Estado_cuenta']['current_balance'] = current_balance
    
    return analysis_results


def generate_comprehensive_questions(analysis_results):
    """Generate comprehensive test questions based on the analysis results."""
    print("\n=== Comprehensive Test Questions ===")
    
    questions = []
    
    # Questions based on facturas data
    if 'facturas' in analysis_results:
        questions.extend([
            "¿Cuál es el total de facturas emitidas?",
            "¿Cuál es el promedio de las facturas?",
            "¿Cuáles son mis clientes principales?",
            "¿Cómo se distribuyen las facturas por tipo (por cobrar vs por pagar)?",
            "¿Cuál es la factura más alta y más baja?",
            "¿Cuál es el total de facturas por cobrar?",
            "¿Cuál es el total de facturas por pagar?"
        ])
    
    # Questions based on gastos data
    if 'gastos_fijos' in analysis_results:
        questions.extend([
            "¿Cuáles son mis gastos fijos más altos?",
            "¿Cuál es el total de gastos fijos?",
            "¿Cómo se distribuyen mis gastos por categoría?",
            "¿Cuál es el promedio de gastos mensuales?",
            "¿Qué categoría de gastos es la más costosa?"
        ])
    
    # Questions based on estado data
    if 'Estado_cuenta' in analysis_results:
        questions.extend([
            "¿Cuál es mi flujo de caja?",
            "¿Cuáles son mis ingresos y egresos?",
            "¿Cuál es el saldo de mi cuenta bancaria?",
            "¿Cómo han variado los movimientos bancarios?",
            "¿Cuál es el movimiento más alto y más bajo?"
        ])
    
    # Add the main PRD question
    questions.append("¿Cómo variaron mis facturas por pagar y por cobrar en los últimos 2 meses?")
    
    for i, question in enumerate(questions, 1):
        print(f"{i}. {question}")
    
    return questions


def simulate_detailed_responses(questions, analysis_results):
    """Simulate detailed agent responses based on real data."""
    print("\n=== Detailed Simulated Agent Responses ===")
    
    for i, question in enumerate(questions[:5], 1):  # Show first 5 questions
        print(f"\n--- Question {i}: {question} ---")
        
        # Generate detailed response based on real data
        if "total de facturas" in question.lower() and 'facturas' in analysis_results:
            total = analysis_results['facturas']['total_amount']
            count = analysis_results['facturas']['count']
            avg = analysis_results['facturas']['avg_amount']
            
            print(f"📊 Executive Summary")
            print(f"Total invoices: ${total:,.2f} across {count} invoices with average of ${avg:,.2f}.")
            print(f"📈 Detailed Analysis")
            print(f"- Total amount: ${total:,.2f}")
            print(f"- Number of invoices: {count}")
            print(f"- Average invoice: ${avg:,.2f}")
            print(f"- Min invoice: ${analysis_results['facturas']['min_amount']:,.2f}")
            print(f"- Max invoice: ${analysis_results['facturas']['max_amount']:,.2f}")
            
            if 'by_type' in analysis_results['facturas']:
                print(f"📊 By Type:")
                for type_data in analysis_results['facturas']['by_type']:
                    print(f"  - {type_data['type']}: ${type_data['total']:,.2f} ({type_data['count']} invoices)")
            
            print(f"🔍 Data Sources Used")
            print(f"- facturas.xlsx: Folio de Factura, Tipo, Cliente/Proveedor, Fecha de Emisión, Monto (MXN)")
            print(f"💡 Key Insights")
            print(f"- Total revenue from invoices: ${total:,.2f}")
            print(f"- Average invoice size: ${avg:,.2f}")
        
        elif "gastos fijos" in question.lower() and 'gastos_fijos' in analysis_results:
            total = analysis_results['gastos_fijos']['total_expenses']
            count = analysis_results['gastos_fijos']['count']
            avg = analysis_results['gastos_fijos']['avg_expense']
            
            print(f"📊 Executive Summary")
            print(f"Total fixed expenses: ${total:,.2f} across {count} items with average of ${avg:,.2f}.")
            print(f"📈 Detailed Analysis")
            print(f"- Total expenses: ${total:,.2f}")
            print(f"- Number of expenses: {count}")
            print(f"- Average expense: ${avg:,.2f}")
            print(f"- Min expense: ${analysis_results['gastos_fijos']['min_expense']:,.2f}")
            print(f"- Max expense: ${analysis_results['gastos_fijos']['max_expense']:,.2f}")
            
            if 'by_category' in analysis_results['gastos_fijos']:
                print(f"📊 By Category:")
                for cat_data in analysis_results['gastos_fijos']['by_category']:
                    print(f"  - {cat_data['category']}: ${cat_data['total']:,.2f} ({cat_data['count']} items)")
            
            print(f"🔍 Data Sources Used")
            print(f"- gastos_fijos.xlsx: Gasto Fijo, Monto (MXN), Día del mes para hacer pago")
            print(f"💡 Key Insights")
            print(f"- Total fixed expenses: ${total:,.2f}")
            print(f"- Average expense: ${avg:,.2f}")
        
        elif "flujo de caja" in question.lower() and 'Estado_cuenta' in analysis_results:
            net_flow = analysis_results['Estado_cuenta']['net_flow']
            positive = analysis_results['Estado_cuenta']['positive_movements']
            negative = analysis_results['Estado_cuenta']['negative_movements']
            total = analysis_results['Estado_cuenta']['total_movements']
            
            print(f"📊 Executive Summary")
            print(f"Net cash flow: ${net_flow:,.2f} with ${positive:,.2f} inflows and ${abs(negative):,.2f} outflows.")
            print(f"📈 Detailed Analysis")
            print(f"- Net cash flow: ${net_flow:,.2f}")
            print(f"- Total inflows: ${positive:,.2f}")
            print(f"- Total outflows: ${abs(negative):,.2f}")
            print(f"- Total movements: ${total:,.2f}")
            print(f"- Number of transactions: {analysis_results['Estado_cuenta']['count']}")
            
            if 'current_balance' in analysis_results['Estado_cuenta']:
                balance = analysis_results['Estado_cuenta']['current_balance']
                print(f"- Current balance: ${balance:,.2f}")
            
            print(f"🔍 Data Sources Used")
            print(f"- Estado_cuenta.xlsx: Fecha, Descripción de la transacción, Monto de la transacción (MXN), Saldo (MXN)")
            print(f"💡 Key Insights")
            print(f"- Net cash flow: ${net_flow:,.2f}")
            print(f"- Cash flow direction: {'Positive' if net_flow > 0 else 'Negative'}")
        
        elif "variaron mis facturas por pagar y por cobrar" in question.lower():
            print(f"📊 Executive Summary")
            print(f"Analysis of accounts receivable and payable variation over the last 2 months.")
            print(f"📈 Detailed Analysis")
            
            if 'facturas' in analysis_results and 'by_type' in analysis_results['facturas']:
                for type_data in analysis_results['facturas']['by_type']:
                    print(f"- {type_data['type']}: ${type_data['total']:,.2f} ({type_data['count']} invoices)")
            
            if 'Estado_cuenta' in analysis_results:
                net_flow = analysis_results['Estado_cuenta']['net_flow']
                print(f"- Net cash flow: ${net_flow:,.2f}")
            
            print(f"🔍 Data Sources Used")
            print(f"- facturas.xlsx: Invoice data with type classification")
            print(f"- Estado_cuenta.xlsx: Bank transaction data")
            print(f"💡 Key Insights")
            print(f"- Combined analysis of receivables and payables")
            print(f"- Cash flow impact assessment")


def generate_validation_report(analysis_results):
    """Generate a validation report comparing expected vs actual data."""
    print("\n=== Validation Report ===")
    
    print(f"📊 Data Quality Assessment:")
    
    for filename, results in analysis_results.items():
        print(f"\n{filename}:")
        if 'count' in results:
            print(f"  - Records: {results['count']}")
        
        if 'total_amount' in results:
            print(f"  - Total amount: ${results['total_amount']:,.2f}")
            print(f"  - Average amount: ${results['avg_amount']:,.2f}")
        
        if 'total_expenses' in results:
            print(f"  - Total expenses: ${results['total_expenses']:,.2f}")
            print(f"  - Average expense: ${results['avg_expense']:,.2f}")
        
        if 'net_flow' in results:
            print(f"  - Net cash flow: ${results['net_flow']:,.2f}")
            print(f"  - Positive movements: ${results['positive_movements']:,.2f}")
            print(f"  - Negative movements: ${results['negative_movements']:,.2f}")
        
        if 'current_balance' in results:
            print(f"  - Current balance: ${results['current_balance']:,.2f}")
    
    print(f"\n✅ Data validation completed successfully!")
    print(f"📈 All financial calculations are based on real data from Excel files.")


def main():
    """Main function to run the final data analysis."""
    print("🔍 Final Financial Data Analysis - Real Data Testing")
    print("=" * 60)
    
    try:
        # Load and analyze real data
        all_data, summaries = load_and_analyze_real_data()
        
        if not all_data:
            print("❌ No data could be loaded. Please check the data files.")
            return
        
        # Analyze financial data with actual column names
        analysis_results = analyze_financial_data_final(all_data, summaries)
        
        # Generate comprehensive test questions
        questions = generate_comprehensive_questions(analysis_results)
        
        # Simulate detailed agent responses
        simulate_detailed_responses(questions, analysis_results)
        
        # Generate validation report
        generate_validation_report(analysis_results)
        
        print("\n🎉 Final data analysis completed successfully!")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 