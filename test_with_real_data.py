"""
Test script for the Financial Agent with real data from the datasets.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime, timedelta
from financial_agent.agent import FinancialAgent
from financial_agent.data_loader import create_data_loader
from financial_agent.financial_analyzer import FinancialAnalyzer
from financial_agent.state import FinancialQuestion

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_and_analyze_real_data():
    """Load and analyze the real Excel files to understand the data structure."""
    print("=== Loading Real Data ===")
    
    data_loader = create_data_loader()
    
    # Load all available files
    all_data = {}
    summaries = {}
    
    for filename in data_loader.available_files:
        print(f"\n--- Analyzing {filename} ---")
        
        df = data_loader.load_file(filename)
        if df is not None:
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
        else:
            print(f"❌ Could not load {filename}")
    
    return all_data, summaries


def create_test_questions_based_on_data(all_data, summaries):
    """Create test questions based on the actual data structure."""
    print("\n=== Creating Test Questions Based on Real Data ===")
    
    test_questions = []
    
    # Analyze facturas.xlsx
    if 'facturas.xlsx' in all_data:
        facturas_df = all_data['facturas.xlsx']
        print(f"\nFacturas data analysis:")
        print(f"  Columns: {list(facturas_df.columns)}")
        print(f"  Date range: {facturas_df['fecha'].min()} to {facturas_df['fecha'].max()}")
        print(f"  Total amount: ${facturas_df['monto'].sum():,.2f}")
        print(f"  Average amount: ${facturas_df['monto'].mean():,.2f}")
        
        # Create questions based on facturas data
        test_questions.extend([
            "¿Cuál es el total de facturas emitidas?",
            "¿Cuál es el promedio de las facturas?",
            "¿Cuáles son mis clientes principales?",
            "¿Cómo han variado las facturas en los últimos meses?",
            "¿Cuál es la factura más alta y más baja?"
        ])
    
    # Analyze gastos_fijos.xlsx
    if 'gastos_fijos.xlsx' in all_data:
        gastos_df = all_data['gastos_fijos.xlsx']
        print(f"\nGastos fijos data analysis:")
        print(f"  Columns: {list(gastos_df.columns)}")
        print(f"  Date range: {gastos_df['fecha'].min()} to {gastos_df['fecha'].max()}")
        print(f"  Total expenses: ${gastos_df['monto'].sum():,.2f}")
        print(f"  Average expense: ${gastos_df['monto'].mean():,.2f}")
        
        if 'rubro' in gastos_df.columns:
            print(f"  Categories: {gastos_df['rubro'].unique()}")
        
        # Create questions based on gastos data
        test_questions.extend([
            "¿Cuáles son mis gastos fijos más altos?",
            "¿Cuál es el total de gastos fijos?",
            "¿Cómo se distribuyen mis gastos por categoría?",
            "¿Cuál es el promedio de gastos mensuales?",
            "¿Qué categoría de gastos es la más costosa?"
        ])
    
    # Analyze Estado_cuenta.xlsx
    if 'Estado_cuenta.xlsx' in all_data:
        estado_df = all_data['Estado_cuenta.xlsx']
        print(f"\nEstado de cuenta data analysis:")
        print(f"  Columns: {list(estado_df.columns)}")
        print(f"  Date range: {estado_df['fecha'].min()} to {estado_df['fecha'].max()}")
        print(f"  Total movements: ${estado_df['monto'].sum():,.2f}")
        print(f"  Positive movements: ${estado_df[estado_df['monto'] > 0]['monto'].sum():,.2f}")
        print(f"  Negative movements: ${estado_df[estado_df['monto'] < 0]['monto'].sum():,.2f}")
        
        # Create questions based on estado data
        test_questions.extend([
            "¿Cuál es mi flujo de caja?",
            "¿Cuáles son mis ingresos y egresos?",
            "¿Cuál es el saldo de mi cuenta bancaria?",
            "¿Cómo han variado los movimientos bancarios?",
            "¿Cuál es el movimiento más alto y más bajo?"
        ])
    
    # Add the main question from the PRD
    test_questions.append("¿Cómo variaron mis facturas por pagar y por cobrar en los últimos 2 meses?")
    
    return test_questions


def run_comprehensive_tests():
    """Run comprehensive tests with real data."""
    print("🚀 Financial Agent - Real Data Testing")
    print("=" * 50)
    
    # Load and analyze real data
    all_data, summaries = load_and_analyze_real_data()
    
    # Create test questions based on real data
    test_questions = create_test_questions_based_on_data(all_data, summaries)
    
    # Initialize the agent
    agent = FinancialAgent()
    
    print(f"\n=== Running {len(test_questions)} Test Questions ===")
    
    results = []
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n--- Test {i}: {question} ---")
        
        try:
            result = agent.process_question_sync(question)
            
            if result["success"]:
                print("✅ Analysis completed successfully!")
                print("Processing steps:", result["processing_steps"])
                
                # Extract the response content
                response_content = ""
                for message in result["response"]:
                    if hasattr(message, 'content'):
                        response_content = message.content
                        break
                
                # Store results for comparison
                results.append({
                    'question': question,
                    'success': True,
                    'response': response_content,
                    'analysis_result': result.get("analysis_result"),
                    'processing_steps': result.get("processing_steps", [])
                })
                
                # Print a summary of the response
                lines = response_content.split('\n')
                summary_lines = [line for line in lines if line.strip() and not line.startswith('#')]
                if summary_lines:
                    print("Response summary:")
                    for line in summary_lines[:5]:  # Show first 5 lines
                        print(f"  {line}")
                
            else:
                print(f"❌ Error: {result['error']}")
                results.append({
                    'question': question,
                    'success': False,
                    'error': result['error']
                })
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            results.append({
                'question': question,
                'success': False,
                'error': str(e)
            })
    
    # Generate test report
    generate_test_report(results, summaries)
    
    return results


def generate_test_report(results, summaries):
    """Generate a comprehensive test report."""
    print("\n" + "=" * 50)
    print("📊 TEST REPORT")
    print("=" * 50)
    
    # Summary statistics
    total_tests = len(results)
    successful_tests = sum(1 for r in results if r['success'])
    failed_tests = total_tests - successful_tests
    
    print(f"Total tests: {total_tests}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success rate: {(successful_tests/total_tests)*100:.1f}%")
    
    # Data summary
    print(f"\n📈 Data Summary:")
    for filename, summary in summaries.items():
        print(f"  {filename}: {summary['rows']} rows, {len(summary['columns'])} columns")
    
    # Failed tests
    if failed_tests > 0:
        print(f"\n❌ Failed Tests:")
        for result in results:
            if not result['success']:
                print(f"  - {result['question']}")
                print(f"    Error: {result['error']}")
    
    # Successful tests analysis
    if successful_tests > 0:
        print(f"\n✅ Successful Tests Analysis:")
        
        # Analyze response patterns
        response_lengths = []
        for result in results:
            if result['success'] and 'response' in result:
                response_lengths.append(len(result['response']))
        
        if response_lengths:
            print(f"  Average response length: {np.mean(response_lengths):.0f} characters")
            print(f"  Min response length: {min(response_lengths)} characters")
            print(f"  Max response length: {max(response_lengths)} characters")
        
        # Check for specific patterns in responses
        cash_flow_mentions = sum(1 for r in results if r['success'] and 'cash flow' in r['response'].lower())
        data_sources_mentions = sum(1 for r in results if r['success'] and 'data sources' in r['response'].lower())
        
        print(f"  Responses mentioning cash flow: {cash_flow_mentions}")
        print(f"  Responses with data sources: {data_sources_mentions}")
    
    print("\n" + "=" * 50)


def test_specific_scenarios():
    """Test specific scenarios based on the PRD requirements."""
    print("\n=== Testing Specific PRD Scenarios ===")
    
    agent = FinancialAgent()
    
    # Test the main PRD question
    main_question = "¿Cómo variaron mis facturas por pagar y por cobrar en los últimos 2 meses?"
    print(f"\n--- Testing Main PRD Question ---")
    print(f"Question: {main_question}")
    
    result = agent.process_question_sync(main_question)
    
    if result["success"]:
        print("✅ PRD question processed successfully!")
        
        # Extract response content
        response_content = ""
        for message in result["response"]:
            if hasattr(message, 'content'):
                response_content = message.content
                break
        
        # Check for required elements
        required_elements = [
            "Executive Summary",
            "Detailed Analysis", 
            "Data Sources Used",
            "Key Insights"
        ]
        
        print("\nChecking required elements:")
        for element in required_elements:
            if element in response_content:
                print(f"  ✅ {element}")
            else:
                print(f"  ❌ {element}")
        
        # Check for quantitative analysis
        if any(word in response_content.lower() for word in ['$', 'total', 'amount', 'sum']):
            print("  ✅ Quantitative analysis present")
        else:
            print("  ❌ Quantitative analysis missing")
        
        # Check for traceability
        if any(word in response_content.lower() for word in ['facturas.xlsx', 'estado_cuenta.xlsx', 'gastos_fijos.xlsx']):
            print("  ✅ Data traceability present")
        else:
            print("  ❌ Data traceability missing")
        
    else:
        print(f"❌ PRD question failed: {result['error']}")


def main():
    """Main function to run all tests."""
    try:
        # Run comprehensive tests
        results = run_comprehensive_tests()
        
        # Test specific PRD scenarios
        test_specific_scenarios()
        
        print("\n🎉 All tests completed!")
        
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 