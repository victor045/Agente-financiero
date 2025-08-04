"""
State management for the Financial Conversational Agent.
"""

from typing import Annotated, Optional, List, Dict, Any
from pydantic import BaseModel, Field
import operator
from langgraph.graph import MessagesState
from langchain_core.messages import MessageLikeRepresentation
from typing_extensions import TypedDict
from datetime import datetime


###################
# Structured Outputs
###################

class FinancialQuestion(BaseModel):
    """Structured output for interpreting financial questions."""
    question_type: str = Field(
        description="Type of financial analysis needed (e.g., 'cash_flow', 'expenses', 'revenue', 'comparison')"
    )
    time_period: Optional[str] = Field(
        description="Time period mentioned in the question (e.g., 'last 2 months', 'Q1 2024')"
    )
    metrics: List[str] = Field(
        description="Key financial metrics to analyze (e.g., ['facturas_por_pagar', 'facturas_por_cobrar'])"
    )
    data_sources: List[str] = Field(
        description="Required data sources for analysis (e.g., ['facturas.xlsx', 'gastos_fijos.xlsx'])"
    )


class DataSourceSelection(BaseModel):
    """Structured output for data source selection."""
    selected_files: List[str] = Field(
        description="List of Excel files to analyze"
    )
    analysis_columns: Dict[str, List[str]] = Field(
        description="Mapping of file names to relevant columns for analysis"
    )
    reasoning: str = Field(
        description="Explanation of why these data sources were selected"
    )


class FinancialAnalysis(BaseModel):
    """Structured output for financial analysis results."""
    summary: str = Field(
        description="Executive summary (BLUF format)"
    )
    detailed_analysis: str = Field(
        description="Detailed financial analysis with calculations"
    )
    data_traceability: Dict[str, List[str]] = Field(
        description="Mapping of analysis components to source files and columns"
    )
    key_insights: List[str] = Field(
        description="Key insights and recommendations"
    )
    calculations: Dict[str, Any] = Field(
        description="Raw calculation data for verification"
    )


###################
# State Definitions
###################

def override_reducer(current_value, new_value):
    """Reducer for overriding state values."""
    if isinstance(new_value, dict) and new_value.get("type") == "override":
        return new_value.get("value", new_value)
    else:
        return operator.add(current_value, new_value)


class FinancialAgentInputState(MessagesState):
    """Input state containing only messages."""
    pass


class FinancialAgentState(MessagesState):
    """Main state for the financial agent."""
    question_interpretation: Optional[FinancialQuestion] = None
    data_selection: Optional[DataSourceSelection] = None
    analysis_result: Optional[FinancialAnalysis] = None
    raw_data: Annotated[Dict[str, Any], override_reducer] = {}
    processing_steps: Annotated[List[str], override_reducer] = []


class QuestionInterpreterState(TypedDict):
    """State for question interpretation phase."""
    messages: Annotated[List[MessageLikeRepresentation], operator.add]
    question_interpretation: Optional[FinancialQuestion]


class DataSelectorState(TypedDict):
    """State for data source selection phase."""
    messages: Annotated[List[MessageLikeRepresentation], operator.add]
    question_interpretation: FinancialQuestion
    available_files: List[str]
    data_selection: Optional[DataSourceSelection]


class FinancialAnalyzerState(TypedDict):
    """State for financial analysis phase."""
    messages: Annotated[List[MessageLikeRepresentation], operator.add]
    question_interpretation: FinancialQuestion
    data_selection: DataSourceSelection
    raw_data: Dict[str, Any]
    analysis_result: Optional[FinancialAnalysis] 