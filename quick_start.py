"""
Quick Start Guide para el Financial Agent.
Ejecuta este script para configurar y probar el agente paso a paso.
"""

import subprocess
import sys
import os
from pathlib import Path


def check_python_version():
    """Verificar versión de Python."""
    print("🐍 Verificando versión de Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True


def install_dependencies():
    """Instalar dependencias necesarias."""
    print("\n📦 Instalando dependencias...")
    
    dependencies = [
        "pandas",
        "numpy", 
        "openpyxl"
    ]
    
    for dep in dependencies:
        try:
            print(f"   Instalando {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"   ✅ {dep} instalado")
        except subprocess.CalledProcessError:
            print(f"   ❌ Error instalando {dep}")
            return False
    
    return True


def check_data_files():
    """Verificar que los archivos de datos estén presentes."""
    print("\n📊 Verificando archivos de datos...")
    
    data_directory = Path("Datasets v2/Datasets v2")
    required_files = [
        "facturas.xlsx",
        "gastos_fijos.xlsx", 
        "Estado_cuenta.xlsx"
    ]
    
    if not data_directory.exists():
        print("❌ Error: Directorio de datos no encontrado")
        print(f"   Buscando en: {data_directory.absolute()}")
        return False
    
    missing_files = []
    for file in required_files:
        file_path = data_directory / file
        if file_path.exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - NO ENCONTRADO")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Faltan {len(missing_files)} archivos:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ Todos los archivos de datos están presentes")
    return True


def run_basic_test():
    """Ejecutar test básico de funcionalidad."""
    print("\n🧪 Ejecutando test básico...")
    
    try:
        # Importar módulos necesarios
        import pandas as pd
        import numpy as np
        from pathlib import Path
        
        print("   ✅ Módulos importados correctamente")
        
        # Test de carga de datos
        data_directory = Path("Datasets v2/Datasets v2")
        facturas_path = data_directory / "facturas.xlsx"
        
        if facturas_path.exists():
            df = pd.read_excel(facturas_path)
            print(f"   ✅ Datos cargados: {len(df)} filas")
            
            # Test de análisis básico
            if 'Monto (MXN)' in df.columns:
                total = df['Monto (MXN)'].sum()
                print(f"   ✅ Análisis básico: ${total:,.2f} MXN")
            else:
                print("   ⚠️  Columna 'Monto (MXN)' no encontrada")
        
        print("   ✅ Test básico completado")
        return True
        
    except Exception as e:
        print(f"   ❌ Error en test básico: {e}")
        return False


def run_full_analysis():
    """Ejecutar análisis completo."""
    print("\n📈 Ejecutando análisis completo...")
    
    try:
        # Ejecutar el script de análisis final
        result = subprocess.run([
            sys.executable, "financial_agent/final_data_test.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Análisis completo ejecutado exitosamente")
            return True
        else:
            print(f"   ❌ Error en análisis: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error ejecutando análisis: {e}")
        return False


def show_next_steps():
    """Mostrar próximos pasos."""
    print("\n" + "=" * 60)
    print("🎯 PRÓXIMOS PASOS")
    print("=" * 60)
    
    print("""
✅ CONFIGURACIÓN COMPLETADA

Ahora puedes:

1. 📊 VER ANÁLISIS DETALLADO:
   python3 financial_agent/final_data_test.py

2. 🎮 EJECUTAR DEMO:
   python3 financial_agent/run_demo.py

3. 📚 LEER DOCUMENTACIÓN:
   - README.md - Guía completa
   - MVP_DOCUMENTATION.md - Detalles técnicos
   - TEST_RESULTS_SUMMARY.md - Resultados de tests

4. 🧪 EJECUTAR TESTS ESPECÍFICOS:
   - financial_agent/simple_data_test.py
   - financial_agent/enhanced_data_test.py
   - financial_agent/validation_tests.py

5. 💡 PROBAR PREGUNTAS:
   - "¿Cuál es el total de facturas emitidas?"
   - "¿Cuáles son mis gastos fijos más altos?"
   - "¿Cuál es mi flujo de caja?"
   - "¿Cómo variaron mis facturas por pagar y por cobrar en los últimos 2 meses?"

🎉 ¡El Financial Agent está listo para usar!
    """)


def main():
    """Función principal del quick start."""
    print("🚀 FINANCIAL AGENT - QUICK START")
    print("=" * 60)
    
    steps = [
        ("Verificar Python", check_python_version),
        ("Instalar dependencias", install_dependencies),
        ("Verificar archivos de datos", check_data_files),
        ("Ejecutar test básico", run_basic_test),
        ("Ejecutar análisis completo", run_full_analysis)
    ]
    
    all_passed = True
    
    for step_name, step_func in steps:
        print(f"\n📋 Paso: {step_name}")
        print("-" * 40)
        
        if step_func():
            print(f"✅ {step_name} - COMPLETADO")
        else:
            print(f"❌ {step_name} - FALLÓ")
            all_passed = False
            break
    
    if all_passed:
        show_next_steps()
    else:
        print("\n❌ CONFIGURACIÓN FALLÓ")
        print("💡 Revisa los errores arriba y vuelve a intentar")


if __name__ == "__main__":
    main() 