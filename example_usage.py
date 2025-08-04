"""
Example usage of the Financial Conversational Agent.

This script demonstrates how to use the financial agent with the provided datasets.
"""

import asyncio
import logging
from financial_agent.agent import FinancialAgent
from financial_agent.data_loader import create_data_loader

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_data_loader():
    """Test the data loader functionality."""
    print("=== Testing Data Loader ===")
    
    data_loader = create_data_loader()
    
    print(f"Available files: {data_loader.available_files}")
    
    # Get summary of all files
    summaries = data_loader.get_all_files_summary()
    
    for filename, summary in summaries.items():
        print(f"\n--- {filename} ---")
        if "error" in summary:
            print(f"Error: {summary['error']}")
        else:
            print(f"Rows: {summary['rows']}")
            print(f"Columns: {summary['columns']}")
            print(f"Sample data: {summary['sample_data'][:2]}")


async def test_financial_agent():
    """Test the financial agent with example questions."""
    print("\n=== Testing Financial Agent ===")
    
    # Initialize agent
    agent = FinancialAgent()
    
    # Example questions from the PRD and similar scenarios
    example_questions = [
        "¿Cómo variaron mis facturas por pagar y por cobrar en los últimos 2 meses?",
        "¿Cuáles son mis gastos fijos más altos?",
        "¿Cuál es el flujo de caja de los últimos 3 meses?",
        "¿Quiénes son mis clientes principales por facturación?",
        "¿Cómo se distribuyen mis gastos por categoría?"
    ]
    
    for i, question in enumerate(example_questions, 1):
        print(f"\n--- Question {i}: {question} ---")
        
        try:
            result = await agent.process_question(question)
            
            if result["success"]:
                print("✅ Analysis completed successfully!")
                print("Processing steps:", result["processing_steps"])
                
                # Print the response
                for message in result["response"]:
                    if hasattr(message, 'content'):
                        print("\n" + message.content)
            else:
                print(f"❌ Error: {result['error']}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")


def test_specific_analysis():
    """Test specific analysis scenarios."""
    print("\n=== Testing Specific Analysis Scenarios ===")
    
    # Test cash flow analysis specifically
    agent = FinancialAgent()
    
    cash_flow_question = "¿Cómo variaron mis facturas por pagar y por cobrar en los últimos 2 meses?"
    
    print(f"Testing cash flow analysis: {cash_flow_question}")
    
    result = agent.process_question_sync(cash_flow_question)
    
    if result["success"]:
        print("✅ Cash flow analysis completed!")
        
        # Show analysis details
        if result.get("analysis_result"):
            analysis = result["analysis_result"]
            print(f"\nSummary: {analysis.summary}")
            print(f"Key insights: {analysis.key_insights}")
            print(f"Data traceability: {analysis.data_traceability}")
    else:
        print(f"❌ Error: {result['error']}")


def main():
    """Main function to run all tests."""
    print("Financial Conversational Agent - Example Usage")
    print("=" * 50)
    
    # Test data loader
    test_data_loader()
    
    # Test financial agent
    asyncio.run(test_financial_agent())
    
    # Test specific analysis
    test_specific_analysis()
    
    print("\n" + "=" * 50)
    print("All tests completed!")


if __name__ == "__main__":
    main() 