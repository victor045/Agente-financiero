# 📋 Instrucciones para Configurar Fuentes de Datos

## 🎯 Opción 1: Configuración Simple (Recomendada)

### Paso 1: Editar el archivo de configuración
Abre el archivo `financial_agent/config_data_sources.py` y cambia esta línea:

```python
data_directory: str = "Datasets v2/Datasets v2"  # ← CAMBIAR ESTA RUTA
```

Por tu ruta de datos, por ejemplo:
```python
data_directory: str = "mi_carpeta_de_datos"  # ← TU RUTA AQUÍ
```

### Paso 2: Usar el agente
```bash
python3 financial_agent/enhanced_financial_agent_with_config.py
```

## 🎯 Opción 2: Configuración Personalizada

### Paso 1: Crear configuración personalizada
```python
from config_data_sources import create_custom_config

# Crear configuración con tu ruta
mi_config = create_custom_config("ruta/a/tus/datos")

# Usar en el agente
from enhanced_financial_agent_with_config import EnhancedFinancialAgentWithConfig
agent = EnhancedFinancialAgentWithConfig(data_source_config=mi_config)
```

## 🎯 Opción 3: Usar Configuraciones Predefinidas

### Paso 1: Editar configuraciones predefinidas
En `financial_agent/config_data_sources.py`, modifica las configuraciones:

```python
CONFIGURATIONS = {
    "default": DataSourceConfig("Datasets v2/Datasets v2"),
    "mi_datos": DataSourceConfig("mi_carpeta_de_datos"),  # ← TU CONFIGURACIÓN
    "excel_files": DataSourceConfig("excel_files"),
    "custom": DataSourceConfig("ruta/personalizada/a/tus/datos")
}
```

### Paso 2: Usar configuración específica
```python
from config_data_sources import get_config
from enhanced_financial_agent_with_config import EnhancedFinancialAgentWithConfig

# Usar configuración específica
config = get_config("mi_datos")
agent = EnhancedFinancialAgentWithConfig(data_source_config=config)
```

## 📁 Estructura de Datos Esperada

El agente espera archivos Excel con estas estructuras:

### facturas.xlsx
- Columnas: Folio de Factura, Tipo, Cliente/Proveedor, Fecha de Emisión, Monto (MXN)
- Tipos: "Por cobrar", "Por pagar"

### gastos_fijos.xlsx
- Columnas: Categoria, Monto, Descripción

### Estado_cuenta.xlsx
- Columnas: Fecha, Tipo, Monto, Descripción

## 🔧 Verificar Configuración

Para verificar que tu configuración funciona:

```bash
python3 financial_agent/config_data_sources.py
```

Esto te mostrará:
- ✅ Archivos encontrados
- ❌ Errores si hay problemas
- 📁 Ruta actual configurada

## 💡 Ejemplos de Uso

### Ejemplo 1: Cambiar a carpeta personalizada
```python
# En config_data_sources.py
data_directory: str = "mis_datos_financieros"
```

### Ejemplo 2: Usar configuración específica
```python
from config_data_sources import get_config
config = get_config("mi_datos")
```

### Ejemplo 3: Crear configuración temporal
```python
from config_data_sources import create_custom_config
config = create_custom_config("datos_temporales")
```

## 🚨 Solución de Problemas

### Error: "No se encontraron archivos de datos"
1. Verifica que la ruta existe
2. Verifica que los archivos tienen extensiones: .xlsx, .csv, .json
3. Verifica que los archivos no están vacíos

### Error: "El directorio no existe"
1. Usa rutas relativas desde el directorio del proyecto
2. O usa rutas absolutas completas
3. Verifica permisos de lectura

### Error: "No se pudo importar config_data_sources.py"
1. Asegúrate de que el archivo existe en `financial_agent/`
2. Verifica que no hay errores de sintaxis en el archivo

## 📞 Comandos Rápidos

```bash
# Verificar configuración actual
python3 financial_agent/config_data_sources.py

# Usar agente con configuración por defecto
python3 financial_agent/enhanced_financial_agent_with_config.py

# Usar agente original (sin configuración externa)
python3 financial_agent/enhanced_financial_agent_simple_viz.py
``` 