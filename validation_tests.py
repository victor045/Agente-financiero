"""
Validation tests that compare agent responses with actual data calculations.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime, timedelta
import re
from financial_agent.agent import FinancialAgent
from financial_agent.data_loader import create_data_loader

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_numbers_from_text(text):
    """Extract numbers from text, including currency amounts."""
    # Pattern to match currency amounts like $1,234.56 or $1,234
    currency_pattern = r'\$[\d,]+\.?\d*'
    numbers = re.findall(currency_pattern, text)
    
    # Convert to float, removing $ and commas
    amounts = []
    for num in numbers:
        try:
            amount = float(num.replace('$', '').replace(',', ''))
            amounts.append(amount)
        except ValueError:
            continue
    
    return amounts


def calculate_actual_totals(data_loader):
    """Calculate actual totals from the real data."""
    print("=== Calculating Actual Totals from Real Data ===")
    
    actual_totals = {}
    
    # Load all files
    for filename in data_loader.available_files:
        df = data_loader.load_file(filename)
        if df is not None:
            print(f"\n--- {filename} ---")
            
            if 'monto' in df.columns:
                total = df['monto'].sum()
                average = df['monto'].mean()
                count = len(df)
                
                actual_totals[filename] = {
                    'total': total,
                    'average': average,
                    'count': count,
                    'min': df['monto'].min(),
                    'max': df['monto'].max()
                }
                
                print(f"  Total: ${total:,.2f}")
                print(f"  Average: ${average:,.2f}")
                print(f"  Count: {count}")
                print(f"  Min: ${df['monto'].min():,.2f}")
                print(f"  Max: ${df['monto'].max():,.2f}")
                
                # Additional analysis based on file type
                if filename == 'facturas.xlsx' and 'cliente' in df.columns:
                    client_totals = df.groupby('cliente')['monto'].sum().sort_values(ascending=False)
                    print(f"  Top clients:")
                    for client, amount in client_totals.head(3).items():
                        print(f"    {client}: ${amount:,.2f}")
                
                elif filename == 'gastos_fijos.xlsx' and 'rubro' in df.columns:
                    category_totals = df.groupby('rubro')['monto'].sum().sort_values(ascending=False)
                    print(f"  Categories:")
                    for category, amount in category_totals.items():
                        print(f"    {category}: ${amount:,.2f}")
                
                elif filename == 'Estado_cuenta.xlsx':
                    positive = df[df['monto'] > 0]['monto'].sum()
                    negative = df[df['monto'] < 0]['monto'].sum()
                    net = positive + negative
                    print(f"  Positive movements: ${positive:,.2f}")
                    print(f"  Negative movements: ${negative:,.2f}")
                    print(f"  Net flow: ${net:,.2f}")
    
    return actual_totals


def validate_agent_response(question, response, actual_totals):
    """Validate that the agent's response matches actual data calculations."""
    print(f"\n=== Validating Response for: {question} ===")
    
    # Extract numbers from response
    response_amounts = extract_numbers_from_text(response)
    print(f"Amounts found in response: {response_amounts}")
    
    # Compare with actual totals
    validation_results = {}
    
    for filename, totals in actual_totals.items():
        print(f"\nChecking {filename}:")
        
        # Check if the response mentions this file
        if filename.lower() in response.lower():
            print(f"  ✅ File mentioned in response")
            
            # Check if total amounts match
            if totals['total'] in response_amounts:
                print(f"  ✅ Total amount ${totals['total']:,.2f} found in response")
                validation_results[filename] = {'total_match': True}
            else:
                print(f"  ❌ Total amount ${totals['total']:,.2f} not found in response")
                validation_results[filename] = {'total_match': False}
            
            # Check if average amounts match
            if totals['average'] in response_amounts:
                print(f"  ✅ Average amount ${totals['average']:,.2f} found in response")
                validation_results[filename]['average_match'] = True
            else:
                print(f"  ❌ Average amount ${totals['average']:,.2f} not found in response")
                validation_results[filename]['average_match'] = False
        else:
            print(f"  ⚠️  File not mentioned in response")
            validation_results[filename] = {'mentioned': False}
    
    return validation_results


def run_validation_tests():
    """Run comprehensive validation tests."""
    print("🔍 Financial Agent - Validation Testing")
    print("=" * 50)
    
    # Initialize components
    data_loader = create_data_loader()
    agent = FinancialAgent()
    
    # Calculate actual totals
    actual_totals = calculate_actual_totals(data_loader)
    
    # Test questions that should produce specific results
    test_cases = [
        {
            'question': "¿Cuál es el total de facturas emitidas?",
            'expected_file': 'facturas.xlsx',
            'expected_calculation': 'total'
        },
        {
            'question': "¿Cuál es el promedio de las facturas?",
            'expected_file': 'facturas.xlsx',
            'expected_calculation': 'average'
        },
        {
            'question': "¿Cuál es el total de gastos fijos?",
            'expected_file': 'gastos_fijos.xlsx',
            'expected_calculation': 'total'
        },
        {
            'question': "¿Cuál es mi flujo de caja?",
            'expected_file': 'Estado_cuenta.xlsx',
            'expected_calculation': 'net_flow'
        },
        {
            'question': "¿Cómo variaron mis facturas por pagar y por cobrar en los últimos 2 meses?",
            'expected_files': ['facturas.xlsx', 'Estado_cuenta.xlsx'],
            'expected_calculation': 'multiple'
        }
    ]
    
    validation_results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Validation Test {i} ---")
        print(f"Question: {test_case['question']}")
        
        try:
            result = agent.process_question_sync(test_case['question'])
            
            if result["success"]:
                # Extract response content
                response_content = ""
                for message in result["response"]:
                    if hasattr(message, 'content'):
                        response_content = message.content
                        break
                
                # Validate response against actual data
                validation = validate_agent_response(
                    test_case['question'], 
                    response_content, 
                    actual_totals
                )
                
                validation_results.append({
                    'test_case': test_case,
                    'success': True,
                    'validation': validation,
                    'response': response_content
                })
                
                # Print validation summary
                print(f"\nValidation Summary:")
                for filename, val_result in validation.items():
                    if 'total_match' in val_result:
                        status = "✅" if val_result['total_match'] else "❌"
                        print(f"  {status} {filename} total amount")
                    if 'average_match' in val_result:
                        status = "✅" if val_result['average_match'] else "❌"
                        print(f"  {status} {filename} average amount")
                
            else:
                print(f"❌ Agent failed: {result['error']}")
                validation_results.append({
                    'test_case': test_case,
                    'success': False,
                    'error': result['error']
                })
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            validation_results.append({
                'test_case': test_case,
                'success': False,
                'error': str(e)
            })
    
    # Generate validation report
    generate_validation_report(validation_results, actual_totals)
    
    return validation_results


def generate_validation_report(validation_results, actual_totals):
    """Generate a comprehensive validation report."""
    print("\n" + "=" * 50)
    print("📊 VALIDATION REPORT")
    print("=" * 50)
    
    # Summary statistics
    total_tests = len(validation_results)
    successful_tests = sum(1 for r in validation_results if r['success'])
    failed_tests = total_tests - successful_tests
    
    print(f"Total validation tests: {total_tests}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success rate: {(successful_tests/total_tests)*100:.1f}%")
    
    # Accuracy analysis
    if successful_tests > 0:
        print(f"\n📈 Accuracy Analysis:")
        
        total_matches = 0
        total_checks = 0
        
        for result in validation_results:
            if result['success'] and 'validation' in result:
                for filename, val_result in result['validation'].items():
                    if 'total_match' in val_result:
                        total_checks += 1
                        if val_result['total_match']:
                            total_matches += 1
                    if 'average_match' in val_result:
                        total_checks += 1
                        if val_result['average_match']:
                            total_matches += 1
        
        if total_checks > 0:
            accuracy = (total_matches / total_checks) * 100
            print(f"  Data accuracy: {accuracy:.1f}% ({total_matches}/{total_checks} matches)")
        else:
            print(f"  No data accuracy checks performed")
    
    # Data summary
    print(f"\n📊 Actual Data Summary:")
    for filename, totals in actual_totals.items():
        print(f"  {filename}:")
        print(f"    Total: ${totals['total']:,.2f}")
        print(f"    Average: ${totals['average']:,.2f}")
        print(f"    Count: {totals['count']}")
    
    # Failed validations
    failed_validations = [r for r in validation_results if not r['success']]
    if failed_validations:
        print(f"\n❌ Failed Validations:")
        for result in failed_validations:
            print(f"  - {result['test_case']['question']}")
            print(f"    Error: {result['error']}")
    
    print("\n" + "=" * 50)


def test_data_quality():
    """Test the quality and consistency of the real data."""
    print("\n=== Data Quality Analysis ===")
    
    data_loader = create_data_loader()
    
    for filename in data_loader.available_files:
        print(f"\n--- {filename} Quality Check ---")
        
        df = data_loader.load_file(filename)
        if df is not None:
            print(f"  Rows: {len(df)}")
            print(f"  Columns: {list(df.columns)}")
            print(f"  Missing values:")
            for col in df.columns:
                missing = df[col].isnull().sum()
                if missing > 0:
                    print(f"    {col}: {missing} missing values")
            
            # Check for data types
            print(f"  Data types:")
            for col, dtype in df.dtypes.items():
                print(f"    {col}: {dtype}")
            
            # Check for date ranges
            if 'fecha' in df.columns:
                print(f"  Date range: {df['fecha'].min()} to {df['fecha'].max()}")
            
            # Check for amount ranges
            if 'monto' in df.columns:
                print(f"  Amount range: ${df['monto'].min():,.2f} to ${df['monto'].max():,.2f}")
                print(f"  Amount distribution:")
                print(f"    Mean: ${df['monto'].mean():,.2f}")
                print(f"    Median: ${df['monto'].median():,.2f}")
                print(f"    Std: ${df['monto'].std():,.2f}")


def main():
    """Main function to run validation tests."""
    try:
        # Run validation tests
        validation_results = run_validation_tests()
        
        # Test data quality
        test_data_quality()
        
        print("\n🎉 Validation tests completed!")
        
    except Exception as e:
        print(f"❌ Validation test execution failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 