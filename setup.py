"""
Setup script for the Financial Conversational Agent.
"""

import os
import sys
import subprocess
from pathlib import Path
from financial_agent.config import FinancialAgentConfig, validate_config


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required")
        sys.exit(1)
    print("✅ Python version is compatible")


def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        sys.exit(1)


def setup_environment():
    """Set up environment variables."""
    print("🔧 Setting up environment...")
    
    env_file = Path(".env")
    env_example = Path("env_example.txt")
    
    if not env_file.exists() and env_example.exists():
        # Copy example to .env
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file with your API keys")
    else:
        print("ℹ️  .env file already exists or template not found")


def validate_data_directory():
    """Validate that the data directory exists and contains expected files."""
    print("📊 Validating data directory...")
    
    config = FinancialAgentConfig()
    data_path = Path(config.data_directory)
    
    if not data_path.exists():
        print(f"❌ Data directory {config.data_directory} does not exist")
        print("Please ensure the data files are in the correct location")
        return False
    
    # Check for expected Excel files
    expected_files = ["facturas.xlsx", "gastos_fijos.xlsx", "Estado_cuenta.xlsx"]
    found_files = []
    
    for file in expected_files:
        if (data_path / file).exists():
            found_files.append(file)
        else:
            print(f"⚠️  Expected file {file} not found")
    
    if found_files:
        print(f"✅ Found {len(found_files)} data files: {', '.join(found_files)}")
        return True
    else:
        print("❌ No expected data files found")
        return False


def test_imports():
    """Test that all required modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        import pandas as pd
        import numpy as np
        from langchain.chat_models import init_chat_model
        from langgraph.graph import StateGraph
        from financial_agent.agent import FinancialAgent
        from financial_agent.data_loader import create_data_loader
        from financial_agent.financial_analyzer import FinancialAnalyzer
        
        print("✅ All required modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def run_basic_test():
    """Run a basic functionality test."""
    print("🧪 Running basic functionality test...")
    
    try:
        # Test data loader
        data_loader = create_data_loader()
        print(f"✅ Data loader initialized with {len(data_loader.available_files)} files")
        
        # Test configuration
        config = FinancialAgentConfig()
        validate_config(config)
        print("✅ Configuration validated")
        
        # Test analyzer
        analyzer = FinancialAnalyzer()
        print("✅ Financial analyzer initialized")
        
        print("✅ Basic functionality test passed")
        return True
        
    except Exception as e:
        print(f"❌ Basic test failed: {e}")
        return False


def main():
    """Main setup function."""
    print("🚀 Financial Agent Setup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Setup environment
    setup_environment()
    
    # Validate data directory
    data_ok = validate_data_directory()
    
    # Test imports
    imports_ok = test_imports()
    
    # Run basic test
    test_ok = run_basic_test()
    
    print("\n" + "=" * 40)
    print("📋 Setup Summary:")
    print(f"✅ Python version: Compatible")
    print(f"✅ Dependencies: Installed")
    print(f"✅ Environment: {'Configured' if data_ok else 'Needs attention'}")
    print(f"✅ Data files: {'Found' if data_ok else 'Missing'}")
    print(f"✅ Imports: {'Working' if imports_ok else 'Failed'}")
    print(f"✅ Basic test: {'Passed' if test_ok else 'Failed'}")
    
    if data_ok and imports_ok and test_ok:
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Edit .env file with your OpenAI API key")
        print("2. Run: python financial_agent/example_usage.py")
        print("3. Start using the financial agent!")
    else:
        print("\n⚠️  Setup completed with issues. Please check the errors above.")


if __name__ == "__main__":
    main() 