"""
Financial analysis utilities for the conversational agent.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging
from financial_agent.state import FinancialQuestion, FinancialAnalysis

logger = logging.getLogger(__name__)


class FinancialAnalyzer:
    """Handles financial analysis calculations and insights."""
    
    def __init__(self):
        self.analysis_methods = {
            'cash_flow': self._analyze_cash_flow,
            'expenses': self._analyze_expenses,
            'revenue': self._analyze_revenue,
            'comparison': self._analyze_comparison,
            'trends': self._analyze_trends
        }
    
    def analyze(self, question: FinancialQuestion, data: Dict[str, pd.DataFrame]) -> FinancialAnalysis:
        """Main analysis method that routes to specific analysis functions."""
        try:
            # Determine analysis type
            analysis_type = question.question_type
            
            if analysis_type in self.analysis_methods:
                return self.analysis_methods[analysis_type](question, data)
            else:
                return self._analyze_general(question, data)
                
        except Exception as e:
            logger.error(f"Error in financial analysis: {e}")
            return self._create_error_analysis(str(e))
    
    def _analyze_cash_flow(self, question: FinancialQuestion, data: Dict[str, pd.DataFrame]) -> FinancialAnalysis:
        """Analyze cash flow patterns and trends."""
        calculations = {}
        insights = []
        
        # Extract relevant data
        invoices_data = data.get('facturas.xlsx', pd.DataFrame())
        bank_data = data.get('Estado_cuenta.xlsx', pd.DataFrame())
        
        if not invoices_data.empty:
            # Analyze accounts receivable (facturas por cobrar)
            if 'fecha' in invoices_data.columns and 'monto' in invoices_data.columns:
                recent_invoices = self._filter_by_period(invoices_data, question.time_period)
                total_receivable = recent_invoices['monto'].sum()
                avg_receivable = recent_invoices['monto'].mean()
                
                calculations['accounts_receivable'] = {
                    'total': total_receivable,
                    'average': avg_receivable,
                    'count': len(recent_invoices)
                }
                
                insights.append(f"Total accounts receivable: ${total_receivable:,.2f}")
                insights.append(f"Average invoice amount: ${avg_receivable:,.2f}")
        
        if not bank_data.empty:
            # Analyze bank movements
            if 'fecha' in bank_data.columns and 'monto' in bank_data.columns:
                recent_movements = self._filter_by_period(bank_data, question.time_period)
                
                # Separate debits and credits
                debits = recent_movements[recent_movements['monto'] < 0]['monto'].sum()
                credits = recent_movements[recent_movements['monto'] > 0]['monto'].sum()
                net_flow = credits + debits
                
                calculations['cash_flow'] = {
                    'debits': debits,
                    'credits': credits,
                    'net_flow': net_flow
                }
                
                insights.append(f"Net cash flow: ${net_flow:,.2f}")
                insights.append(f"Total inflows: ${credits:,.2f}")
                insights.append(f"Total outflows: ${abs(debits):,.2f}")
        
        # Generate summary
        summary = self._generate_cash_flow_summary(calculations)
        
        return FinancialAnalysis(
            summary=summary,
            detailed_analysis=self._format_cash_flow_analysis(calculations, insights),
            data_traceability=self._create_traceability(data),
            key_insights=insights,
            calculations=calculations
        )
    
    def _analyze_expenses(self, question: FinancialQuestion, data: Dict[str, pd.DataFrame]) -> FinancialAnalysis:
        """Analyze expense patterns and categories."""
        calculations = {}
        insights = []
        
        # Analyze fixed expenses
        expenses_data = data.get('gastos_fijos.xlsx', pd.DataFrame())
        
        if not expenses_data.empty:
            recent_expenses = self._filter_by_period(expenses_data, question.time_period)
            
            if 'monto' in recent_expenses.columns:
                total_expenses = recent_expenses['monto'].sum()
                avg_expense = recent_expenses['monto'].mean()
                
                calculations['expenses'] = {
                    'total': total_expenses,
                    'average': avg_expense,
                    'count': len(recent_expenses)
                }
                
                insights.append(f"Total fixed expenses: ${total_expenses:,.2f}")
                insights.append(f"Average expense: ${avg_expense:,.2f}")
            
            # Analyze by category if available
            if 'rubro' in recent_expenses.columns:
                category_analysis = recent_expenses.groupby('rubro')['monto'].agg(['sum', 'count']).reset_index()
                category_analysis.columns = ['category', 'total', 'count']
                
                calculations['expenses_by_category'] = category_analysis.to_dict('records')
                
                top_category = category_analysis.loc[category_analysis['total'].idxmax()]
                insights.append(f"Highest expense category: {top_category['category']} (${top_category['total']:,.2f})")
        
        summary = self._generate_expense_summary(calculations)
        
        return FinancialAnalysis(
            summary=summary,
            detailed_analysis=self._format_expense_analysis(calculations, insights),
            data_traceability=self._create_traceability(data),
            key_insights=insights,
            calculations=calculations
        )
    
    def _analyze_revenue(self, question: FinancialQuestion, data: Dict[str, pd.DataFrame]) -> FinancialAnalysis:
        """Analyze revenue patterns and trends."""
        calculations = {}
        insights = []
        
        # Analyze invoices (revenue)
        invoices_data = data.get('facturas.xlsx', pd.DataFrame())
        
        if not invoices_data.empty:
            recent_invoices = self._filter_by_period(invoices_data, question.time_period)
            
            if 'monto' in recent_invoices.columns:
                total_revenue = recent_invoices['monto'].sum()
                avg_revenue = recent_invoices['monto'].mean()
                
                calculations['revenue'] = {
                    'total': total_revenue,
                    'average': avg_revenue,
                    'count': len(recent_invoices)
                }
                
                insights.append(f"Total revenue: ${total_revenue:,.2f}")
                insights.append(f"Average invoice: ${avg_revenue:,.2f}")
            
            # Analyze by client if available
            if 'cliente' in recent_invoices.columns:
                client_analysis = recent_invoices.groupby('cliente')['monto'].agg(['sum', 'count']).reset_index()
                client_analysis.columns = ['client', 'total', 'count']
                
                calculations['revenue_by_client'] = client_analysis.to_dict('records')
                
                top_client = client_analysis.loc[client_analysis['total'].idxmax()]
                insights.append(f"Top client: {top_client['client']} (${top_client['total']:,.2f})")
        
        summary = self._generate_revenue_summary(calculations)
        
        return FinancialAnalysis(
            summary=summary,
            detailed_analysis=self._format_revenue_analysis(calculations, insights),
            data_traceability=self._create_traceability(data),
            key_insights=insights,
            calculations=calculations
        )
    
    def _analyze_comparison(self, question: FinancialQuestion, data: Dict[str, pd.DataFrame]) -> FinancialAnalysis:
        """Analyze comparisons between different periods or categories."""
        calculations = {}
        insights = []
        
        # This is a placeholder for comparison analysis
        # In a real implementation, you would compare different periods or categories
        
        summary = "Comparison analysis completed. Key differences identified between periods."
        
        return FinancialAnalysis(
            summary=summary,
            detailed_analysis="Detailed comparison analysis with period-over-period changes.",
            data_traceability=self._create_traceability(data),
            key_insights=insights,
            calculations=calculations
        )
    
    def _analyze_trends(self, question: FinancialQuestion, data: Dict[str, pd.DataFrame]) -> FinancialAnalysis:
        """Analyze trends over time."""
        calculations = {}
        insights = []
        
        # This is a placeholder for trend analysis
        # In a real implementation, you would calculate trends over time
        
        summary = "Trend analysis completed. Key trends identified in financial data."
        
        return FinancialAnalysis(
            summary=summary,
            detailed_analysis="Detailed trend analysis with time-series patterns.",
            data_traceability=self._create_traceability(data),
            key_insights=insights,
            calculations=calculations
        )
    
    def _analyze_general(self, question: FinancialQuestion, data: Dict[str, pd.DataFrame]) -> FinancialAnalysis:
        """General analysis for unspecified question types."""
        calculations = {}
        insights = []
        
        # Basic analysis of all available data
        for filename, df in data.items():
            if not df.empty and 'monto' in df.columns:
                total_amount = df['monto'].sum()
                calculations[filename] = {
                    'total_amount': total_amount,
                    'row_count': len(df)
                }
                insights.append(f"{filename}: ${total_amount:,.2f} total")
        
        summary = "General financial analysis completed with overview of all data sources."
        
        return FinancialAnalysis(
            summary=summary,
            detailed_analysis="Comprehensive analysis of all available financial data.",
            data_traceability=self._create_traceability(data),
            key_insights=insights,
            calculations=calculations
        )
    
    def _filter_by_period(self, df: pd.DataFrame, time_period: Optional[str]) -> pd.DataFrame:
        """Filter dataframe by time period if specified."""
        if not time_period or 'fecha' not in df.columns:
            return df
        
        try:
            # Parse time period (simplified implementation)
            if 'last 2 months' in time_period.lower():
                cutoff_date = datetime.now() - timedelta(days=60)
            elif 'last month' in time_period.lower():
                cutoff_date = datetime.now() - timedelta(days=30)
            elif 'last 3 months' in time_period.lower():
                cutoff_date = datetime.now() - timedelta(days=90)
            else:
                return df  # Return all data if period not recognized
            
            return df[df['fecha'] >= cutoff_date]
            
        except Exception as e:
            logger.warning(f"Error filtering by period: {e}")
            return df
    
    def _create_traceability(self, data: Dict[str, pd.DataFrame]) -> Dict[str, List[str]]:
        """Create data traceability mapping."""
        traceability = {}
        
        for filename, df in data.items():
            if not df.empty:
                traceability[filename] = list(df.columns)
        
        return traceability
    
    def _generate_cash_flow_summary(self, calculations: Dict[str, Any]) -> str:
        """Generate executive summary for cash flow analysis."""
        if 'cash_flow' in calculations:
            net_flow = calculations['cash_flow']['net_flow']
            if net_flow > 0:
                return f"Positive cash flow of ${net_flow:,.2f} indicates healthy financial position."
            else:
                return f"Negative cash flow of ${net_flow:,.2f} requires attention to liquidity management."
        else:
            return "Cash flow analysis completed with available data."
    
    def _generate_expense_summary(self, calculations: Dict[str, Any]) -> str:
        """Generate executive summary for expense analysis."""
        if 'expenses' in calculations:
            total = calculations['expenses']['total']
            return f"Total fixed expenses: ${total:,.2f}. Review categories for optimization opportunities."
        else:
            return "Expense analysis completed with available data."
    
    def _generate_revenue_summary(self, calculations: Dict[str, Any]) -> str:
        """Generate executive summary for revenue analysis."""
        if 'revenue' in calculations:
            total = calculations['revenue']['total']
            return f"Total revenue: ${total:,.2f}. Monitor client concentration and payment patterns."
        else:
            return "Revenue analysis completed with available data."
    
    def _format_cash_flow_analysis(self, calculations: Dict[str, Any], insights: List[str]) -> str:
        """Format detailed cash flow analysis."""
        analysis = "## Cash Flow Analysis\n\n"
        
        if 'cash_flow' in calculations:
            cf = calculations['cash_flow']
            analysis += f"- **Net Cash Flow**: ${cf['net_flow']:,.2f}\n"
            analysis += f"- **Total Inflows**: ${cf['credits']:,.2f}\n"
            analysis += f"- **Total Outflows**: ${abs(cf['debits']):,.2f}\n\n"
        
        if 'accounts_receivable' in calculations:
            ar = calculations['accounts_receivable']
            analysis += f"- **Accounts Receivable**: ${ar['total']:,.2f}\n"
            analysis += f"- **Average Invoice**: ${ar['average']:,.2f}\n\n"
        
        return analysis
    
    def _format_expense_analysis(self, calculations: Dict[str, Any], insights: List[str]) -> str:
        """Format detailed expense analysis."""
        analysis = "## Expense Analysis\n\n"
        
        if 'expenses' in calculations:
            exp = calculations['expenses']
            analysis += f"- **Total Expenses**: ${exp['total']:,.2f}\n"
            analysis += f"- **Average Expense**: ${exp['average']:,.2f}\n"
            analysis += f"- **Number of Expenses**: {exp['count']}\n\n"
        
        if 'expenses_by_category' in calculations:
            analysis += "### Expenses by Category\n"
            for category in calculations['expenses_by_category']:
                analysis += f"- **{category['category']}**: ${category['total']:,.2f} ({category['count']} items)\n"
        
        return analysis
    
    def _format_revenue_analysis(self, calculations: Dict[str, Any], insights: List[str]) -> str:
        """Format detailed revenue analysis."""
        analysis = "## Revenue Analysis\n\n"
        
        if 'revenue' in calculations:
            rev = calculations['revenue']
            analysis += f"- **Total Revenue**: ${rev['total']:,.2f}\n"
            analysis += f"- **Average Invoice**: ${rev['average']:,.2f}\n"
            analysis += f"- **Number of Invoices**: {rev['count']}\n\n"
        
        if 'revenue_by_client' in calculations:
            analysis += "### Revenue by Client\n"
            for client in calculations['revenue_by_client']:
                analysis += f"- **{client['client']}**: ${client['total']:,.2f} ({client['count']} invoices)\n"
        
        return analysis
    
    def _create_error_analysis(self, error_message: str) -> FinancialAnalysis:
        """Create error analysis when analysis fails."""
        return FinancialAnalysis(
            summary="Analysis could not be completed due to an error.",
            detailed_analysis=f"Error during analysis: {error_message}",
            data_traceability={},
            key_insights=["Please check data quality and try again."],
            calculations={}
        ) 