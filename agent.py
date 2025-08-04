"""
Main Financial Conversational Agent using LangGraph.
"""

import asyncio
from typing import Dict, List, Any, Literal
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import START, END, StateGraph
from langgraph.types import Command
import logging

from financial_agent.state import (
    FinancialAgentState,
    FinancialAgentInputState,
    QuestionInterpreterState,
    DataSelectorState,
    FinancialAnalyzerState,
    FinancialQuestion,
    DataSourceSelection,
    FinancialAnalysis
)
from financial_agent.prompts import (
    QUESTION_INTERPRETATION_PROMPT,
    DATA_SOURCE_SELECTION_PROMPT,
    FINANCIAL_ANALYSIS_PROMPT,
    RESPONSE_FORMATTING_PROMPT
)
from financial_agent.data_loader import create_data_loader
from financial_agent.financial_analyzer import FinancialAnalyzer

logger = logging.getLogger(__name__)

# Initialize configurable model
configurable_model = init_chat_model(
    configurable_fields=("model", "max_tokens", "api_key"),
)


async def interpret_question(state: FinancialAgentInputState, config: RunnableConfig) -> Command[Literal["select_data_sources", "__end__"]]:
    """Interpret the user's financial question using LLM."""
    try:
        # Get the user's question from messages
        messages = state.get("messages", [])
        if not messages:
            return Command(goto=END, update={"messages": [AIMessage(content="No question provided. Please ask a financial question.")]})
        
        user_question = messages[-1].content if hasattr(messages[-1], 'content') else str(messages[-1])
        
        # Configure model for question interpretation
        model_config = {
            "model": "gpt-4o-mini",  # Can be made configurable
            "max_tokens": 1000,
            "api_key": config.get("api_key"),
            "tags": ["financial_agent:question_interpretation"]
        }
        
        model = configurable_model.with_structured_output(FinancialQuestion).with_config(model_config)
        
        # Create prompt with user question
        prompt = QUESTION_INTERPRETATION_PROMPT.format(user_question=user_question)
        
        response = await model.ainvoke([HumanMessage(content=prompt)])
        
        logger.info(f"Question interpreted: {response.question_type}")
        
        return Command(
            goto="select_data_sources",
            update={
                "question_interpretation": response,
                "processing_steps": ["Question interpreted successfully"]
            }
        )
        
    except Exception as e:
        logger.error(f"Error interpreting question: {e}")
        return Command(
            goto=END,
            update={
                "messages": [AIMessage(content=f"Error interpreting your question: {str(e)}. Please try rephrasing your question.")]
            }
        )


async def select_data_sources(state: QuestionInterpreterState, config: RunnableConfig) -> Command[Literal["load_and_analyze", "__end__"]]:
    """Select relevant data sources based on the interpreted question."""
    try:
        question_interpretation = state.get("question_interpretation")
        if not question_interpretation:
            return Command(goto=END, update={"messages": [AIMessage(content="No question interpretation available.")]})
        
        # Initialize data loader
        data_loader = create_data_loader()
        available_files = data_loader.available_files
        
        # Configure model for data source selection
        model_config = {
            "model": "gpt-4o-mini",
            "max_tokens": 1000,
            "api_key": config.get("api_key"),
            "tags": ["financial_agent:data_selection"]
        }
        
        model = configurable_model.with_structured_output(DataSourceSelection).with_config(model_config)
        
        # Create prompt with question interpretation and available files
        prompt = DATA_SOURCE_SELECTION_PROMPT.format(
            question_interpretation=str(question_interpretation),
            available_files=", ".join(available_files)
        )
        
        response = await model.ainvoke([HumanMessage(content=prompt)])
        
        logger.info(f"Selected data sources: {response.selected_files}")
        
        return Command(
            goto="load_and_analyze",
            update={
                "data_selection": response,
                "available_files": available_files,
                "processing_steps": ["Data sources selected successfully"]
            }
        )
        
    except Exception as e:
        logger.error(f"Error selecting data sources: {e}")
        return Command(
            goto=END,
            update={
                "messages": [AIMessage(content=f"Error selecting data sources: {str(e)}. Please try again.")]
            }
        )


async def load_and_analyze(state: DataSelectorState, config: RunnableConfig) -> Command[Literal["format_response", "__end__"]]:
    """Load data and perform financial analysis."""
    try:
        question_interpretation = state.get("question_interpretation")
        data_selection = state.get("data_selection")
        
        if not question_interpretation or not data_selection:
            return Command(goto=END, update={"messages": [AIMessage(content="Missing question interpretation or data selection.")]})
        
        # Load data
        data_loader = create_data_loader()
        raw_data = data_loader.load_multiple_files(data_selection.selected_files)
        
        if not raw_data:
            return Command(
                goto=END,
                update={
                    "messages": [AIMessage(content="No data could be loaded from the selected sources. Please check the data files.")]
                }
            )
        
        # Perform analysis
        analyzer = FinancialAnalyzer()
        analysis_result = analyzer.analyze(question_interpretation, raw_data)
        
        logger.info("Financial analysis completed successfully")
        
        return Command(
            goto="format_response",
            update={
                "analysis_result": analysis_result,
                "raw_data": raw_data,
                "processing_steps": ["Data loaded and analysis completed"]
            }
        )
        
    except Exception as e:
        logger.error(f"Error in load and analyze: {e}")
        return Command(
            goto=END,
            update={
                "messages": [AIMessage(content=f"Error during analysis: {str(e)}. Please try again.")]
            }
        )


async def format_response(state: FinancialAnalyzerState, config: RunnableConfig) -> Command[Literal["__end__"]]:
    """Format the analysis results into a clear response."""
    try:
        analysis_result = state.get("analysis_result")
        if not analysis_result:
            return Command(goto=END, update={"messages": [AIMessage(content="No analysis results available.")]})
        
        # Configure model for response formatting
        model_config = {
            "model": "gpt-4o-mini",
            "max_tokens": 2000,
            "api_key": config.get("api_key"),
            "tags": ["financial_agent:response_formatting"]
        }
        
        model = configurable_model.with_config(model_config)
        
        # Create formatted response
        formatted_response = f"""## 📊 Executive Summary

{analysis_result.summary}

## 📈 Detailed Analysis

{analysis_result.detailed_analysis}

## 🔍 Data Sources Used

"""
        
        # Add data traceability
        for source, columns in analysis_result.data_traceability.items():
            formatted_response += f"- **{source}**: {', '.join(columns)}\n"
        
        formatted_response += f"""

## 💡 Key Insights & Recommendations

"""
        
        for insight in analysis_result.key_insights:
            formatted_response += f"- {insight}\n"
        
        formatted_response += f"""

## 📋 Technical Details

Raw calculations and methodologies are available for verification in the analysis results.

---
*Analysis completed using financial data from the specified sources.*"""
        
        logger.info("Response formatted successfully")
        
        return Command(
            goto=END,
            update={
                "messages": [AIMessage(content=formatted_response)],
                "processing_steps": ["Response formatted and ready"]
            }
        )
        
    except Exception as e:
        logger.error(f"Error formatting response: {e}")
        return Command(
            goto=END,
            update={
                "messages": [AIMessage(content=f"Error formatting response: {str(e)}. Please try again.")]
            }
        )


def create_financial_agent() -> StateGraph:
    """Create the financial agent workflow."""
    
    # Create the workflow
    workflow = StateGraph(FinancialAgentState)
    
    # Add nodes
    workflow.add_node("interpret_question", interpret_question)
    workflow.add_node("select_data_sources", select_data_sources)
    workflow.add_node("load_and_analyze", load_and_analyze)
    workflow.add_node("format_response", format_response)
    
    # Set entry point
    workflow.set_entry_point("interpret_question")
    
    # Add edges
    workflow.add_edge("interpret_question", "select_data_sources")
    workflow.add_edge("select_data_sources", "load_and_analyze")
    workflow.add_edge("load_and_analyze", "format_response")
    workflow.add_edge("format_response", END)
    
    # Add conditional edges for error handling
    workflow.add_conditional_edges(
        "interpret_question",
        lambda x: "select_data_sources" if x.get("question_interpretation") else "__end__"
    )
    
    workflow.add_conditional_edges(
        "select_data_sources",
        lambda x: "load_and_analyze" if x.get("data_selection") else "__end__"
    )
    
    workflow.add_conditional_edges(
        "load_and_analyze",
        lambda x: "format_response" if x.get("analysis_result") else "__end__"
    )
    
    return workflow.compile()


class FinancialAgent:
    """Main financial agent class."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.workflow = create_financial_agent()
    
    async def process_question(self, question: str) -> Dict[str, Any]:
        """Process a financial question and return the analysis."""
        try:
            # Create initial state
            initial_state = FinancialAgentInputState(messages=[HumanMessage(content=question)])
            
            # Configure the run
            config = {"api_key": self.api_key} if self.api_key else {}
            
            # Run the workflow
            result = await self.workflow.ainvoke(initial_state, config)
            
            return {
                "success": True,
                "response": result.get("messages", []),
                "analysis_result": result.get("analysis_result"),
                "processing_steps": result.get("processing_steps", [])
            }
            
        except Exception as e:
            logger.error(f"Error processing question: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": [AIMessage(content=f"Error processing your question: {str(e)}")]
            }
    
    def process_question_sync(self, question: str) -> Dict[str, Any]:
        """Synchronous wrapper for process_question."""
        return asyncio.run(self.process_question(question))


# Example usage
if __name__ == "__main__":
    # Example usage
    agent = FinancialAgent()
    
    # Example question from the PRD
    question = "¿Cómo variaron mis facturas por pagar y por cobrar en los últimos 2 meses?"
    
    result = agent.process_question_sync(question)
    
    if result["success"]:
        print("Analysis completed successfully!")
        for message in result["response"]:
            if hasattr(message, 'content'):
                print(message.content)
    else:
        print(f"Error: {result['error']}") 