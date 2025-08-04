"""
Unit tests for the data loader functionality.
"""

import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import patch, MagicMock
from financial_agent.data_loader import FinancialDataLoader, create_data_loader


class TestFinancialDataLoader:
    """Test cases for FinancialDataLoader."""
    
    def test_init_with_valid_directory(self):
        """Test initialization with valid data directory."""
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.glob', return_value=[Path('test.xlsx')]):
                loader = FinancialDataLoader("test_directory")
                assert loader.data_directory == Path("test_directory")
    
    def test_init_with_invalid_directory(self):
        """Test initialization with invalid data directory."""
        with patch('pathlib.Path.exists', return_value=False):
            loader = FinancialDataLoader("invalid_directory")
            assert len(loader.available_files) == 0
    
    def test_discover_files(self):
        """Test file discovery functionality."""
        mock_files = [Path('facturas.xlsx'), Path('gastos_fijos.xlsx')]
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.glob', return_value=mock_files):
                loader = FinancialDataLoader("test_directory")
                assert len(loader.available_files) == 2
                assert 'facturas.xlsx' in loader.available_files
                assert 'gastos_fijos.xlsx' in loader.available_files
    
    def test_clean_column_names(self):
        """Test column name cleaning functionality."""
        loader = FinancialDataLoader()
        
        # Test basic cleaning
        columns = pd.Index(['Cliente ', 'Fecha', 'Monto'])
        cleaned = loader._clean_column_names(columns)
        assert cleaned == ['cliente', 'fecha', 'monto']
        
        # Test with special characters
        columns = pd.Index(['Cliente@', 'Fecha#', 'Monto$'])
        cleaned = loader._clean_column_names(columns)
        assert cleaned == ['cliente', 'fecha', 'monto']
    
    def test_handle_missing_values_facturas(self):
        """Test missing value handling for invoices."""
        loader = FinancialDataLoader()
        
        # Create test data with missing values
        df = pd.DataFrame({
            'cliente': ['A', 'B', None],
            'fecha': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'monto': [100, 200, 300]
        })
        
        result = loader._handle_missing_values(df, 'facturas.xlsx')
        assert len(result) == 2  # Should drop row with missing cliente
    
    def test_handle_missing_values_gastos_fijos(self):
        """Test missing value handling for fixed expenses."""
        loader = FinancialDataLoader()
        
        # Create test data with missing amounts
        df = pd.DataFrame({
            'rubro': ['A', 'B', 'C'],
            'fecha': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'monto': [100, None, 300]
        })
        
        result = loader._handle_missing_values(df, 'gastos_fijos.xlsx')
        assert result['monto'].isna().sum() == 0  # Should fill with 0
    
    def test_standardize_dates(self):
        """Test date standardization."""
        loader = FinancialDataLoader()
        
        # Create test data with dates
        df = pd.DataFrame({
            'fecha': ['2024-01-01', '2024-01-02', 'invalid_date'],
            'monto': [100, 200, 300]
        })
        
        result = loader._standardize_dates(df, 'test.xlsx')
        assert pd.api.types.is_datetime64_any_dtype(result['fecha'])
        assert len(result) == 2  # Should drop invalid date
    
    def test_clean_numeric_columns(self):
        """Test numeric column cleaning."""
        loader = FinancialDataLoader()
        
        # Create test data with numeric values
        df = pd.DataFrame({
            'monto': ['100', '200.50', 'invalid', '300'],
            'saldo': ['1000', '2000', '3000', 'invalid']
        })
        
        result = loader._clean_numeric_columns(df, 'test.xlsx')
        assert pd.api.types.is_numeric_dtype(result['monto'])
        assert pd.api.types.is_numeric_dtype(result['saldo'])
        assert result['monto'].isna().sum() == 0  # Should fill with 0
    
    @patch('pandas.read_excel')
    def test_load_file_success(self, mock_read_excel):
        """Test successful file loading."""
        # Mock successful file read
        mock_df = pd.DataFrame({
            'cliente': ['A', 'B'],
            'fecha': ['2024-01-01', '2024-01-02'],
            'monto': [100, 200]
        })
        mock_read_excel.return_value = mock_df
        
        with patch('pathlib.Path.exists', return_value=True):
            loader = FinancialDataLoader()
            result = loader.load_file('test.xlsx')
            
            assert result is not None
            assert len(result) == 2
            assert list(result.columns) == ['cliente', 'fecha', 'monto']
    
    @patch('pandas.read_excel')
    def test_load_file_error(self, mock_read_excel):
        """Test file loading error handling."""
        # Mock file read error
        mock_read_excel.side_effect = Exception("File read error")
        
        with patch('pathlib.Path.exists', return_value=True):
            loader = FinancialDataLoader()
            result = loader.load_file('test.xlsx')
            
            assert result is None
    
    def test_load_multiple_files(self):
        """Test loading multiple files."""
        loader = FinancialDataLoader()
        
        # Mock successful file loading
        with patch.object(loader, 'load_file') as mock_load:
            mock_load.side_effect = [
                pd.DataFrame({'col1': [1, 2]}),
                pd.DataFrame({'col2': [3, 4]})
            ]
            
            result = loader.load_multiple_files(['file1.xlsx', 'file2.xlsx'])
            
            assert len(result) == 2
            assert 'file1.xlsx' in result
            assert 'file2.xlsx' in result
    
    def test_get_file_summary(self):
        """Test file summary generation."""
        loader = FinancialDataLoader()
        
        # Mock successful file loading
        test_df = pd.DataFrame({
            'cliente': ['A', 'B'],
            'fecha': ['2024-01-01', '2024-01-02'],
            'monto': [100, 200]
        })
        
        with patch.object(loader, 'load_file', return_value=test_df):
            summary = loader.get_file_summary('test.xlsx')
            
            assert summary['filename'] == 'test.xlsx'
            assert summary['rows'] == 2
            assert summary['columns'] == ['cliente', 'fecha', 'monto']
            assert len(summary['sample_data']) == 2
    
    def test_get_file_summary_error(self):
        """Test file summary generation with error."""
        loader = FinancialDataLoader()
        
        with patch.object(loader, 'load_file', return_value=None):
            summary = loader.get_file_summary('test.xlsx')
            
            assert 'error' in summary
            assert 'Could not load test.xlsx' in summary['error']


class TestCreateDataLoader:
    """Test cases for create_data_loader factory function."""
    
    def test_create_data_loader_default(self):
        """Test creating data loader with default parameters."""
        loader = create_data_loader()
        assert isinstance(loader, FinancialDataLoader)
        assert loader.data_directory == Path("Datasets v2/Datasets v2")
    
    def test_create_data_loader_custom(self):
        """Test creating data loader with custom directory."""
        loader = create_data_loader("custom_directory")
        assert isinstance(loader, FinancialDataLoader)
        assert loader.data_directory == Path("custom_directory")


if __name__ == "__main__":
    pytest.main([__file__]) 