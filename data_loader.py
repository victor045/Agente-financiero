"""
Data loading and preprocessing utilities for financial data.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging
from datetime import datetime, timedelta
import re

logger = logging.getLogger(__name__)


class FinancialDataLoader:
    """Handles loading and preprocessing of financial Excel files."""
    
    def __init__(self, data_directory: str = "Datasets v2/Datasets v2"):
        self.data_directory = Path(data_directory)
        self.available_files = self._discover_files()
    
    def _discover_files(self) -> List[str]:
        """Discover available Excel files in the data directory."""
        if not self.data_directory.exists():
            logger.warning(f"Data directory {self.data_directory} does not exist")
            return []
        
        excel_files = list(self.data_directory.glob("*.xlsx"))
        return [f.name for f in excel_files]
    
    def load_file(self, filename: str) -> Optional[pd.DataFrame]:
        """Load a single Excel file with error handling."""
        try:
            file_path = self.data_directory / filename
            if not file_path.exists():
                logger.error(f"File {filename} not found")
                return None
            
            # Load Excel file
            df = pd.read_excel(file_path)
            
            # Basic preprocessing
            df = self._preprocess_dataframe(df, filename)
            
            logger.info(f"Successfully loaded {filename} with {len(df)} rows and {len(df.columns)} columns")
            return df
            
        except Exception as e:
            logger.error(f"Error loading {filename}: {str(e)}")
            return None
    
    def _preprocess_dataframe(self, df: pd.DataFrame, filename: str) -> pd.DataFrame:
        """Preprocess dataframe with common data quality fixes."""
        # Make a copy to avoid modifying original
        df = df.copy()
        
        # Clean column names
        df.columns = self._clean_column_names(df.columns)
        
        # Handle missing values
        df = self._handle_missing_values(df, filename)
        
        # Standardize date columns
        df = self._standardize_dates(df, filename)
        
        # Clean numeric columns
        df = self._clean_numeric_columns(df, filename)
        
        return df
    
    def _clean_column_names(self, columns: pd.Index) -> List[str]:
        """Clean and standardize column names."""
        cleaned_columns = []
        
        for col in columns:
            # Remove extra spaces and special characters
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
    
    def _handle_missing_values(self, df: pd.DataFrame, filename: str) -> pd.DataFrame:
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
    
    def _standardize_dates(self, df: pd.DataFrame, filename: str) -> pd.DataFrame:
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
    
    def _clean_numeric_columns(self, df: pd.DataFrame, filename: str) -> pd.DataFrame:
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
    
    def load_multiple_files(self, filenames: List[str]) -> Dict[str, pd.DataFrame]:
        """Load multiple Excel files."""
        data = {}
        
        for filename in filenames:
            df = self.load_file(filename)
            if df is not None:
                data[filename] = df
        
        return data
    
    def get_file_summary(self, filename: str) -> Dict[str, Any]:
        """Get a summary of a file's structure and content."""
        df = self.load_file(filename)
        if df is None:
            return {"error": f"Could not load {filename}"}
        
        summary = {
            "filename": filename,
            "rows": len(df),
            "columns": list(df.columns),
            "column_types": df.dtypes.to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "sample_data": df.head(3).to_dict('records')
        }
        
        return summary
    
    def get_all_files_summary(self) -> Dict[str, Dict[str, Any]]:
        """Get summary of all available files."""
        summaries = {}
        
        for filename in self.available_files:
            summaries[filename] = self.get_file_summary(filename)
        
        return summaries


def create_data_loader(data_directory: str = "Datasets v2/Datasets v2") -> FinancialDataLoader:
    """Factory function to create a data loader instance."""
    return FinancialDataLoader(data_directory) 