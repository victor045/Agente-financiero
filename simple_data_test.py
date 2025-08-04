"""
Simplified test script to analyze real Excel data without complex dependencies.
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
    """Load and analyze the real Excel files to understand the data structure."""
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
            
            # Basic preprocessing
            df = preprocess_dataframe(df, filename)
            
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


def preprocess_dataframe(df, filename):
    """Preprocess dataframe with basic cleaning."""
    df = df.copy()
    
    # Clean column names
    df.columns = clean_column_names(df.columns)
    
    # Handle missing values
    df = handle_missing_values(df, filename)
    
    # Standardize date columns
    df = standardize_dates(df, filename)
    
    # Clean numeric columns
    df = clean_numeric_columns(df, filename)
    
    return df


def clean_column_names(columns):
    """Clean and standardize column names."""
    cleaned_columns = []
    
    for col in columns:
        # Remove extra spaces and special characters
        import re
        cleaned = re.sub(r'[^\w\s]', '', str(col))
        cleaned = re.sub(r'\s+', '_', cleaned.strip())
        cleaned = cleaned.lower()
        
        # Standardize common financial terms
        column_mapping = {
            'cliente': 'cliente',
            'fecha': 'fecha',
            'monto': 'monto',
            'rubro': 'rubro',
            'tipo': 'tipo',
            'descripcion': 'descripcion',
            'saldo': 'saldo',
            'debito': 'debito',
            'credito': 'credito'
        }
        
        cleaned_columns.append(column_mapping.get(cleaned, cleaned))
    
    return cleaned_columns


def handle_missing_values(df, filename):
    """Handle missing values based on file type."""
    if 'facturas' in filename.lower():
        # For invoices, drop rows with missing critical data
        critical_cols = ['cliente', 'fecha', 'monto']
        df = df.dropna(subset=[col for col in critical_cols if col in df.columns])
    
    elif 'gastos_fijos' in filename.lower():
        # For fixed expenses, fill missing amounts with 0
        if 'monto' in df.columns:
            df['monto'] = df['monto'].fillna(0)
    
    elif 'estado_cuenta' in filename.lower():
        # For bank statements, handle missing amounts
        if 'monto' in df.columns:
            df['monto'] = df['monto'].fillna(0)
    
    return df


def standardize_dates(df, filename):
    """Standardize date columns."""
    date_columns = [col for col in df.columns if 'fecha' in col.lower()]
    
    for col in date_columns:
        try:
            # Convert to datetime, handling various formats
            df[col] = pd.to_datetime(df[col], errors='coerce')
            
            # Remove rows with invalid dates
            df = df.dropna(subset=[col])
            
        except Exception as e:
            logger.warning(f"Could not standardize date column {col} in {filename}: {e}")
    
    return df


def clean_numeric_columns(df, filename):
    """Clean numeric columns, especially amounts."""
    numeric_columns = [col for col in df.columns if 'monto' in col.lower() or 'saldo' in col.lower()]
    
    for col in numeric_columns:
        try:
            # Convert to numeric, handling currency symbols and commas
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Fill missing values with 0 for amounts
            df[col] = df[col].fillna(0)
            
        except Exception as e:
            logger.warning(f"Could not clean numeric column {col} in {filename}: {e}")
    
    return df


def analyze_financial_data(all_data, summaries):
    """Analyze financial data and generate insights."""
    print("\n=== Financial Data Analysis ===")
    
    analysis_results = {}
    
    # Analyze facturas.xlsx
    if 'facturas.xlsx' in all_data:
        facturas_df = all_data['facturas.xlsx']
        print(f"\n📊 Facturas Analysis:")
        print(f"  Total invoices: {len(facturas_df)}")
        
        if 'monto' in facturas_df.columns:
            total_amount = facturas_df['monto'].sum()
            avg_amount = facturas_df['monto'].mean()
            print(f"  Total amount: ${total_amount:,.2f}")
            print(f"  Average amount: ${avg_amount:,.2f}")
            print(f"  Min amount: ${facturas_df['monto'].min():,.2f}")
            print(f"  Max amount: ${facturas_df['monto'].max():,.2f}")
            
            analysis_results['facturas'] = {
                'total_amount': total_amount,
                'avg_amount': avg_amount,
                'count': len(facturas_df),
                'min_amount': facturas_df['monto'].min(),
                'max_amount': facturas_df['monto'].max()
            }
        
        if 'cliente' in facturas_df.columns:
            client_analysis = facturas_df.groupby('cliente')['monto'].agg(['sum', 'count']).reset_index()
            client_analysis.columns = ['client', 'total', 'count']
            client_analysis = client_analysis.sort_values('total', ascending=False)
            
            print(f"  Top clients:")
            for _, row in client_analysis.head(5).iterrows():
                print(f"    {row['client']}: ${row['total']:,.2f} ({row['count']} invoices)")
        
        if 'fecha' in facturas_df.columns:
            print(f"  Date range: {facturas_df['fecha'].min()} to {facturas_df['fecha'].max()}")
    
    # Analyze gastos_fijos.xlsx
    if 'gastos_fijos.xlsx' in all_data:
        gastos_df = all_data['gastos_fijos.xlsx']
        print(f"\n💰 Gastos Fijos Analysis:")
        print(f"  Total expenses: {len(gastos_df)}")
        
        if 'monto' in gastos_df.columns:
            total_expenses = gastos_df['monto'].sum()
            avg_expense = gastos_df['monto'].mean()
            print(f"  Total expenses: ${total_expenses:,.2f}")
            print(f"  Average expense: ${avg_expense:,.2f}")
            print(f"  Min expense: ${gastos_df['monto'].min():,.2f}")
            print(f"  Max expense: ${gastos_df['monto'].max():,.2f}")
            
            analysis_results['gastos_fijos'] = {
                'total_expenses': total_expenses,
                'avg_expense': avg_expense,
                'count': len(gastos_df),
                'min_expense': gastos_df['monto'].min(),
                'max_expense': gastos_df['monto'].max()
            }
        
        if 'rubro' in gastos_df.columns:
            category_analysis = gastos_df.groupby('rubro')['monto'].agg(['sum', 'count']).reset_index()
            category_analysis.columns = ['category', 'total', 'count']
            category_analysis = category_analysis.sort_values('total', ascending=False)
            
            print(f"  Categories:")
            for _, row in category_analysis.iterrows():
                print(f"    {row['category']}: ${row['total']:,.2f} ({row['count']} items)")
        
        if 'fecha' in gastos_df.columns:
            print(f"  Date range: {gastos_df['fecha'].min()} to {gastos_df['fecha'].max()}")
    
    # Analyze Estado_cuenta.xlsx
    if 'Estado_cuenta.xlsx' in all_data:
        estado_df = all_data['Estado_cuenta.xlsx']
        print(f"\n🏦 Estado de Cuenta Analysis:")
        print(f"  Total movements: {len(estado_df)}")
        
        if 'monto' in estado_df.columns:
            total_movements = estado_df['monto'].sum()
            positive_movements = estado_df[estado_df['monto'] > 0]['monto'].sum()
            negative_movements = estado_df[estado_df['monto'] < 0]['monto'].sum()
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
        
        if 'fecha' in estado_df.columns:
            print(f"  Date range: {estado_df['fecha'].min()} to {estado_df['fecha'].max()}")
    
    return analysis_results


def generate_test_questions(analysis_results):
    """Generate test questions based on the analysis results."""
    print("\n=== Generated Test Questions ===")
    
    questions = []
    
    # Questions based on facturas data
    if 'facturas' in analysis_results:
        questions.extend([
            "¿Cuál es el total de facturas emitidas?",
            "¿Cuál es el promedio de las facturas?",
            "¿Cuáles son mis clientes principales?",
            "¿Cómo han variado las facturas en los últimos meses?",
            "¿Cuál es la factura más alta y más baja?"
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


def simulate_agent_responses(questions, analysis_results):
    """Simulate what the agent responses should look like based on real data."""
    print("\n=== Simulated Agent Responses ===")
    
    for i, question in enumerate(questions[:3], 1):  # Show first 3 questions
        print(f"\n--- Question {i}: {question} ---")
        
        # Generate simulated response based on real data
        if "total de facturas" in question.lower() and 'facturas' in analysis_results:
            total = analysis_results['facturas']['total_amount']
            count = analysis_results['facturas']['count']
            print(f"Simulated Response:")
            print(f"📊 Executive Summary")
            print(f"Total invoices: ${total:,.2f} across {count} invoices.")
            print(f"📈 Detailed Analysis")
            print(f"- Total amount: ${total:,.2f}")
            print(f"- Number of invoices: {count}")
            print(f"- Average invoice: ${analysis_results['facturas']['avg_amount']:,.2f}")
            print(f"🔍 Data Sources Used")
            print(f"- facturas.xlsx: cliente, fecha, monto")
            print(f"💡 Key Insights")
            print(f"- Total revenue from invoices: ${total:,.2f}")
        
        elif "gastos fijos" in question.lower() and 'gastos_fijos' in analysis_results:
            total = analysis_results['gastos_fijos']['total_expenses']
            count = analysis_results['gastos_fijos']['count']
            print(f"Simulated Response:")
            print(f"📊 Executive Summary")
            print(f"Total fixed expenses: ${total:,.2f} across {count} items.")
            print(f"📈 Detailed Analysis")
            print(f"- Total expenses: ${total:,.2f}")
            print(f"- Number of expenses: {count}")
            print(f"- Average expense: ${analysis_results['gastos_fijos']['avg_expense']:,.2f}")
            print(f"🔍 Data Sources Used")
            print(f"- gastos_fijos.xlsx: rubro, fecha, monto")
            print(f"💡 Key Insights")
            print(f"- Total fixed expenses: ${total:,.2f}")
        
        elif "flujo de caja" in question.lower() and 'Estado_cuenta' in analysis_results:
            net_flow = analysis_results['Estado_cuenta']['net_flow']
            positive = analysis_results['Estado_cuenta']['positive_movements']
            negative = analysis_results['Estado_cuenta']['negative_movements']
            print(f"Simulated Response:")
            print(f"📊 Executive Summary")
            print(f"Net cash flow: ${net_flow:,.2f}.")
            print(f"📈 Detailed Analysis")
            print(f"- Net cash flow: ${net_flow:,.2f}")
            print(f"- Total inflows: ${positive:,.2f}")
            print(f"- Total outflows: ${abs(negative):,.2f}")
            print(f"🔍 Data Sources Used")
            print(f"- Estado_cuenta.xlsx: fecha, monto, tipo")
            print(f"💡 Key Insights")
            print(f"- Net cash flow: ${net_flow:,.2f}")


def main():
    """Main function to run the simplified data analysis."""
    print("🔍 Financial Data Analysis - Real Data Testing")
    print("=" * 50)
    
    try:
        # Load and analyze real data
        all_data, summaries = load_and_analyze_real_data()
        
        if not all_data:
            print("❌ No data could be loaded. Please check the data files.")
            return
        
        # Analyze financial data
        analysis_results = analyze_financial_data(all_data, summaries)
        
        # Generate test questions
        questions = generate_test_questions(analysis_results)
        
        # Simulate agent responses
        simulate_agent_responses(questions, analysis_results)
        
        print("\n🎉 Data analysis completed successfully!")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 