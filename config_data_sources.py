"""
Configuración de Fuentes de Datos para el Financial Agent.
Archivo simple para cambiar las fuentes de datos fácilmente.
"""

from pathlib import Path
from dataclasses import dataclass
from typing import List

@dataclass
class DataSourceConfig:
    """Configuración de fuentes de datos."""
    
    # CAMBIAR AQUÍ LA RUTA DE TUS DATOS
    data_directory: str = "Datasets v2/Datasets v2"  # ← CAMBIAR ESTA RUTA
    
    # Tipos de archivos soportados
    supported_file_types: List[str] = None
    
    def __post_init__(self):
        if self.supported_file_types is None:
            self.supported_file_types = [".xlsx", ".csv", ".json"]
    
    def get_data_directory_path(self) -> Path:
        """Obtener la ruta del directorio de datos."""
        return Path(self.data_directory)
    
    def scan_available_files(self) -> List[str]:
        """Escanear archivos disponibles."""
        data_path = self.get_data_directory_path()
        available_files = []
        
        if not data_path.exists():
            print(f"❌ Error: El directorio {data_path} no existe")
            return []
        
        for file_path in data_path.glob("*"):
            if file_path.suffix.lower() in self.supported_file_types:
                available_files.append(file_path.name)
        
        return available_files
    
    def show_data_info(self):
        """Mostrar información sobre las fuentes de datos."""
        print("\n📊 CONFIGURACIÓN DE FUENTES DE DATOS")
        print("=" * 50)
        print(f"📁 Directorio actual: {self.data_directory}")
        
        available_files = self.scan_available_files()
        print(f"📋 Archivos disponibles: {len(available_files)}")
        
        if available_files:
            print("\n📄 Archivos encontrados:")
            for i, file in enumerate(available_files, 1):
                print(f"   {i}. {file}")
        else:
            print("❌ No se encontraron archivos de datos")
            print("💡 Verifica que:")
            print("   - El directorio existe")
            print("   - Los archivos tienen extensiones: .xlsx, .csv, .json")
            print("   - Los archivos no están vacíos")
        
        print("\n🔧 Para cambiar las fuentes de datos:")
        print("   1. Modifica 'data_directory' en este archivo")
        print("   2. O crea una nueva instancia con tu configuración")
        print("=" * 50)


# Configuraciones predefinidas
CONFIGURATIONS = {
    "default": DataSourceConfig("Datasets v2/Datasets v2"),
    "mi_datos": DataSourceConfig("mi_carpeta_de_datos"),
    "excel_files": DataSourceConfig("excel_files"),
    "custom": DataSourceConfig("ruta/personalizada/a/tus/datos")
}


def get_config(config_name: str = "default") -> DataSourceConfig:
    """Obtener configuración por nombre."""
    return CONFIGURATIONS.get(config_name, CONFIGURATIONS["default"])


def create_custom_config(data_directory: str) -> DataSourceConfig:
    """Crear configuración personalizada."""
    return DataSourceConfig(data_directory)


if __name__ == "__main__":
    # Ejemplo de uso
    print("🎯 CONFIGURADOR DE FUENTES DE DATOS")
    print("=" * 50)
    
    # Mostrar configuración actual
    config = get_config("default")
    config.show_data_info()
    
    # Ejemplo de cómo cambiar la configuración
    print("\n💡 EJEMPLOS DE USO:")
    print("1. Usar configuración predefinida:")
    print("   config = get_config('default')")
    
    print("\n2. Crear configuración personalizada:")
    print("   config = create_custom_config('mi/ruta/personalizada')")
    
    print("\n3. Cambiar en el agente:")
    print("   from config_data_sources import get_config")
    print("   config = get_config('mi_datos')")
    print("   agent = EnhancedFinancialAgentSimpleViz(config)") 