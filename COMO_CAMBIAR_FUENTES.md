# 🎯 Cómo Cambiar las Fuentes de Datos

## 📁 Opción 1: Cambiar en el archivo (Más Fácil)

### Paso 1: Abrir el archivo
Abre `financial_agent/enhanced_financial_agent_configurable.py`

### Paso 2: Cambiar la línea 49
Busca esta línea:
```python
data_directory: str = "Datasets v2/Datasets v2"  # ← CAMBIAR ESTA RUTA
```

### Paso 3: Cambiar por tu ruta
Por ejemplo:
```python
data_directory: str = "mi_carpeta_de_datos"  # ← TU RUTA AQUÍ
```

### Paso 4: Usar el agente
```bash
python3 financial_agent/enhanced_financial_agent_configurable.py
```

## 📁 Opción 2: Usar el agente original

Si prefieres usar el agente original que funciona:

### Paso 1: Cambiar en el archivo original
Abre `financial_agent/enhanced_financial_agent_simple_viz.py`

### Paso 2: Cambiar la línea 49
Busca esta línea:
```python
data_directory: str = "Datasets v2/Datasets v2"
```

### Paso 3: Cambiar por tu ruta
```python
data_directory: str = "mi_carpeta_de_datos"
```

### Paso 4: Usar el agente
```bash
python3 financial_agent/enhanced_financial_agent_simple_viz.py
```

## 📋 Ejemplos de Rutas

```python
# Carpeta en el mismo directorio
data_directory: str = "mis_datos"

# Carpeta en subdirectorio
data_directory: str = "datos/financieros"

# Ruta absoluta (completa)
data_directory: str = "/home/usuario/mis_datos"

# Carpeta con espacios
data_directory: str = "Mis Datos Financieros"
```

## 🚨 Solución de Problemas

### Error: "No se encontraron archivos"
- Verifica que la carpeta existe
- Verifica que tiene archivos .xlsx, .csv, .json
- Verifica que los archivos no están vacíos

### Error: "El directorio no existe"
- Usa rutas relativas desde el directorio del proyecto
- O usa rutas absolutas completas
- Verifica permisos de lectura

## 📞 Comandos Rápidos

```bash
# Usar agente configurable
python3 financial_agent/enhanced_financial_agent_configurable.py

# Usar agente original
python3 financial_agent/enhanced_financial_agent_simple_viz.py
```

## 💡 Tip

Solo necesitas cambiar **UNA LÍNEA** en cualquiera de los dos archivos para cambiar las fuentes de datos. 