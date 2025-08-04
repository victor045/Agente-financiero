"""
Interactive Financial Agent - Haz preguntas y obtén respuestas basadas en datos reales.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime, timedelta

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InteractiveFinancialAgent:
    """Agente financiero interactivo que responde preguntas basadas en datos reales."""
    
    def __init__(self):
        self.data_directory = Path("Datasets v2/Datasets v2")
        self.data = {}
        self.last_analysis = {}
        self.load_data()
    
    def load_data(self):
        """Cargar todos los datos de Excel."""
        print("📊 Cargando datos financieros...")
        
        # Cargar facturas
        facturas_path = self.data_directory / "facturas.xlsx"
        if facturas_path.exists():
            self.data['facturas'] = pd.read_excel(facturas_path)
            print(f"✅ facturas.xlsx: {len(self.data['facturas'])} facturas")
        
        # Cargar gastos fijos
        gastos_path = self.data_directory / "gastos_fijos.xlsx"
        if gastos_path.exists():
            self.data['gastos_fijos'] = pd.read_excel(gastos_path)
            print(f"✅ gastos_fijos.xlsx: {len(self.data['gastos_fijos'])} gastos")
        
        # Cargar estado de cuenta
        estado_path = self.data_directory / "Estado_cuenta.xlsx"
        if estado_path.exists():
            self.data['Estado_cuenta'] = pd.read_excel(estado_path)
            print(f"✅ Estado_cuenta.xlsx: {len(self.data['Estado_cuenta'])} movimientos")
    
    def analyze_facturas(self):
        """Analizar datos de facturas."""
        if 'facturas' not in self.data:
            return {}
        
        df = self.data['facturas']
        analysis = {}
        
        if 'Monto (MXN)' in df.columns:
            analysis['total'] = df['Monto (MXN)'].sum()
            analysis['promedio'] = df['Monto (MXN)'].mean()
            analysis['min'] = df['Monto (MXN)'].min()
            analysis['max'] = df['Monto (MXN)'].max()
            analysis['count'] = len(df)
        
        if 'Tipo' in df.columns and 'Monto (MXN)' in df.columns:
            # Análisis por tipo
            por_cobrar = df[df['Tipo'] == 'Por cobrar']['Monto (MXN)'].sum()
            por_pagar = df[df['Tipo'] == 'Por pagar']['Monto (MXN)'].sum()
            analysis['por_cobrar'] = por_cobrar
            analysis['por_pagar'] = por_pagar
            
            # Análisis detallado por tipo
            facturas_por_cobrar = df[df['Tipo'] == 'Por cobrar']
            facturas_por_pagar = df[df['Tipo'] == 'Por pagar']
            
            if not facturas_por_cobrar.empty:
                analysis['por_cobrar_max'] = facturas_por_cobrar['Monto (MXN)'].max()
                analysis['por_cobrar_min'] = facturas_por_cobrar['Monto (MXN)'].min()
                analysis['por_cobrar_count'] = len(facturas_por_cobrar)
                analysis['por_cobrar_promedio'] = facturas_por_cobrar['Monto (MXN)'].mean()
                
                # Detalles de la factura más alta por cobrar
                max_cobrar_idx = facturas_por_cobrar['Monto (MXN)'].idxmax()
                analysis['por_cobrar_max_details'] = {
                    'folio': facturas_por_cobrar.loc[max_cobrar_idx, 'Folio de Factura'] if 'Folio de Factura' in facturas_por_cobrar.columns else 'N/A',
                    'cliente': facturas_por_cobrar.loc[max_cobrar_idx, 'Cliente/Proveedor'] if 'Cliente/Proveedor' in facturas_por_cobrar.columns else 'N/A',
                    'fecha': facturas_por_cobrar.loc[max_cobrar_idx, 'Fecha de Emisión'] if 'Fecha de Emisión' in facturas_por_cobrar.columns else 'N/A',
                    'monto': facturas_por_cobrar.loc[max_cobrar_idx, 'Monto (MXN)']
                }
            
            if not facturas_por_pagar.empty:
                analysis['por_pagar_max'] = facturas_por_pagar['Monto (MXN)'].max()
                analysis['por_pagar_min'] = facturas_por_pagar['Monto (MXN)'].min()
                analysis['por_pagar_count'] = len(facturas_por_pagar)
                analysis['por_pagar_promedio'] = facturas_por_pagar['Monto (MXN)'].mean()
                
                # Detalles de la factura más alta por pagar
                max_pagar_idx = facturas_por_pagar['Monto (MXN)'].idxmax()
                analysis['por_pagar_max_details'] = {
                    'folio': facturas_por_pagar.loc[max_pagar_idx, 'Folio de Factura'] if 'Folio de Factura' in facturas_por_pagar.columns else 'N/A',
                    'proveedor': facturas_por_pagar.loc[max_pagar_idx, 'Cliente/Proveedor'] if 'Cliente/Proveedor' in facturas_por_pagar.columns else 'N/A',
                    'fecha': facturas_por_pagar.loc[max_pagar_idx, 'Fecha de Emisión'] if 'Fecha de Emisión' in facturas_por_pagar.columns else 'N/A',
                    'monto': facturas_por_pagar.loc[max_pagar_idx, 'Monto (MXN)']
                }
        
        if 'Cliente/Proveedor' in df.columns and 'Monto (MXN)' in df.columns:
            clientes = df.groupby('Cliente/Proveedor')['Monto (MXN)'].agg(['sum', 'count']).reset_index()
            clientes.columns = ['cliente', 'total', 'count']
            clientes = clientes.sort_values('total', ascending=False)
            analysis['top_clientes'] = clientes.head(5).to_dict('records')
        
        return analysis
    
    def analyze_gastos(self):
        """Analizar datos de gastos fijos."""
        if 'gastos_fijos' not in self.data:
            return {}
        
        df = self.data['gastos_fijos']
        analysis = {}
        
        if 'Monto (MXN)' in df.columns:
            analysis['total'] = df['Monto (MXN)'].sum()
            analysis['promedio'] = df['Monto (MXN)'].mean()
            analysis['count'] = len(df)
        
        if 'Gasto Fijo' in df.columns and 'Monto (MXN)' in df.columns:
            categorias = df.groupby('Gasto Fijo')['Monto (MXN)'].sum().reset_index()
            categorias = categorias.sort_values('Monto (MXN)', ascending=False)
            analysis['categorias'] = categorias.to_dict('records')
        
        return analysis
    
    def analyze_estado_cuenta(self):
        """Analizar datos del estado de cuenta."""
        if 'Estado_cuenta' not in self.data:
            return {}
        
        df = self.data['Estado_cuenta']
        analysis = {}
        
        if 'Monto de la transacción (MXN)' in df.columns:
            ingresos = df[df['Monto de la transacción (MXN)'] > 0]['Monto de la transacción (MXN)'].sum()
            egresos = df[df['Monto de la transacción (MXN)'] < 0]['Monto de la transacción (MXN)'].sum()
            neto = ingresos + egresos
            
            analysis['ingresos'] = ingresos
            analysis['egresos'] = egresos
            analysis['neto'] = neto
            analysis['count'] = len(df)
        
        if 'Saldo (MXN)' in df.columns:
            analysis['saldo_actual'] = df['Saldo (MXN)'].iloc[-1]
        
        return analysis
    
    def answer_question(self, question):
        """Responder a una pregunta específica."""
        question_lower = question.lower()
        
        # Análisis de facturas
        if any(word in question_lower for word in ['factura', 'facturas', 'emitida', 'emitidas']):
            return self.answer_facturas_question(question)
        
        # Análisis de gastos
        elif any(word in question_lower for word in ['gasto', 'gastos', 'fijo', 'fijos']):
            return self.answer_gastos_question(question)
        
        # Análisis de estado de cuenta
        elif any(word in question_lower for word in ['flujo', 'caja', 'ingreso', 'egreso', 'saldo', 'cuenta']):
            return self.answer_estado_question(question)
        
        # Análisis combinado
        elif any(word in question_lower for word in ['variaron', 'últimos', 'meses', 'cobrar', 'pagar']):
            return self.answer_combined_question(question)
        
        # Preguntas de seguimiento sobre cantidades específicas
        elif any(word in question_lower for word in ['cantidad', 'peso', 'monto', 'cuánto', 'cuanto', 'valor']):
            return self.answer_followup_question(question)
        
        else:
            return self.answer_general_question(question)
    
    def answer_facturas_question(self, question):
        """Responder preguntas sobre facturas."""
        analysis = self.analyze_facturas()
        self.last_analysis = analysis  # Guardar para preguntas de seguimiento
        question_lower = question.lower()
        
        # Preguntas sobre facturas por pagar específicamente
        if 'por pagar' in question_lower and 'alta' in question_lower:
            if 'por_pagar_max' in analysis:
                details = analysis.get('por_pagar_max_details', {})
                return f"""
📊 Executive Summary
La factura por pagar más alta es: ${analysis['por_pagar_max']:,.2f} MXN

📈 Detailed Analysis
- Factura por pagar más alta: ${analysis['por_pagar_max']:,.2f} MXN
- Proveedor: {details.get('proveedor', 'N/A')}
- Folio: {details.get('folio', 'N/A')}
- Fecha: {details.get('fecha', 'N/A')}
- Total facturas por pagar: {analysis['por_pagar_count']}
- Promedio facturas por pagar: ${analysis['por_pagar_promedio']:,.2f} MXN
- Total por pagar: ${analysis['por_pagar']:,.2f} MXN

🔍 Data Sources Used
- facturas.xlsx: Tipo, Monto (MXN) - Filtrado por "Por pagar"

💡 Key Insights
- La factura por pagar más alta representa ${(analysis['por_pagar_max']/analysis['por_pagar']*100):.1f}% del total por pagar
- Cantidad específica: ${analysis['por_pagar_max']:,.2f} pesos mexicanos
"""
        
        elif 'por pagar' in question_lower and 'baja' in question_lower:
            if 'por_pagar_min' in analysis:
                return f"""
📊 Executive Summary
La factura por pagar más baja es: ${analysis['por_pagar_min']:,.2f} MXN

📈 Detailed Analysis
- Factura por pagar más baja: ${analysis['por_pagar_min']:,.2f} MXN
- Factura por pagar más alta: ${analysis['por_pagar_max']:,.2f} MXN
- Rango facturas por pagar: ${analysis['por_pagar_min']:,.2f} - ${analysis['por_pagar_max']:,.2f} MXN
- Total facturas por pagar: {analysis['por_pagar_count']}

🔍 Data Sources Used
- facturas.xlsx: Tipo, Monto (MXN) - Filtrado por "Por pagar"

💡 Key Insights
- La diferencia entre la factura más alta y más baja es: ${analysis['por_pagar_max'] - analysis['por_pagar_min']:,.2f} MXN
- Cantidad específica: ${analysis['por_pagar_min']:,.2f} pesos mexicanos
"""
        
        elif 'por cobrar' in question_lower and 'alta' in question_lower:
            if 'por_cobrar_max' in analysis:
                details = analysis.get('por_cobrar_max_details', {})
                return f"""
📊 Executive Summary
La factura por cobrar más alta es: ${analysis['por_cobrar_max']:,.2f} MXN

📈 Detailed Analysis
- Factura por cobrar más alta: ${analysis['por_cobrar_max']:,.2f} MXN
- Cliente: {details.get('cliente', 'N/A')}
- Folio: {details.get('folio', 'N/A')}
- Fecha: {details.get('fecha', 'N/A')}
- Total facturas por cobrar: {analysis['por_cobrar_count']}
- Promedio facturas por cobrar: ${analysis['por_cobrar_promedio']:,.2f} MXN
- Total por cobrar: ${analysis['por_cobrar']:,.2f} MXN

🔍 Data Sources Used
- facturas.xlsx: Tipo, Monto (MXN) - Filtrado por "Por cobrar"

💡 Key Insights
- La factura por cobrar más alta representa ${(analysis['por_cobrar_max']/analysis['por_cobrar']*100):.1f}% del total por cobrar
- Cantidad específica: ${analysis['por_cobrar_max']:,.2f} pesos mexicanos
"""
        
        elif 'por cobrar' in question_lower and 'baja' in question_lower:
            if 'por_cobrar_min' in analysis:
                return f"""
📊 Executive Summary
La factura por cobrar más baja es: ${analysis['por_cobrar_min']:,.2f} MXN

📈 Detailed Analysis
- Factura por cobrar más baja: ${analysis['por_cobrar_min']:,.2f} MXN
- Factura por cobrar más alta: ${analysis['por_cobrar_max']:,.2f} MXN
- Rango facturas por cobrar: ${analysis['por_cobrar_min']:,.2f} - ${analysis['por_cobrar_max']:,.2f} MXN
- Total facturas por cobrar: {analysis['por_cobrar_count']}

🔍 Data Sources Used
- facturas.xlsx: Tipo, Monto (MXN) - Filtrado por "Por cobrar"

💡 Key Insights
- La diferencia entre la factura más alta y más baja es: ${analysis['por_cobrar_max'] - analysis['por_cobrar_min']:,.2f} MXN
- Cantidad específica: ${analysis['por_cobrar_min']:,.2f} pesos mexicanos
"""
        
        # Preguntas generales sobre facturas
        elif 'total' in question_lower:
            return f"""
📊 Executive Summary
Total de facturas emitidas: ${analysis['total']:,.2f} MXN

📈 Detailed Analysis
- Total facturas: ${analysis['total']:,.2f} MXN
- Número de facturas: {analysis['count']}
- Promedio por factura: ${analysis['promedio']:,.2f} MXN
- Factura más alta: ${analysis['max']:,.2f} MXN
- Factura más baja: ${analysis['min']:,.2f} MXN

🔍 Data Sources Used
- facturas.xlsx: Folio de Factura, Tipo, Cliente/Proveedor, Fecha de Emisión, Monto (MXN)

💡 Key Insights
- Total de ingresos por facturas: ${analysis['total']:,.2f} MXN
- Promedio de factura: ${analysis['promedio']:,.2f} MXN
- Cantidad específica: ${analysis['total']:,.2f} pesos mexicanos
"""
        
        elif 'promedio' in question_lower:
            return f"""
📊 Executive Summary
Promedio de facturas: ${analysis['promedio']:,.2f} MXN

📈 Detailed Analysis
- Promedio por factura: ${analysis['promedio']:,.2f} MXN
- Total facturas: {analysis['count']}
- Rango: ${analysis['min']:,.2f} - ${analysis['max']:,.2f} MXN

🔍 Data Sources Used
- facturas.xlsx: Monto (MXN)

💡 Key Insights
- El promedio de factura es ${analysis['promedio']:,.2f} MXN
- Cantidad específica: ${analysis['promedio']:,.2f} pesos mexicanos
"""
        
        elif 'cliente' in question_lower or 'clientes' in question_lower:
            if 'top_clientes' in analysis:
                response = f"""
📊 Executive Summary
Top 5 clientes principales por facturación

📈 Detailed Analysis
"""
                for i, cliente in enumerate(analysis['top_clientes'], 1):
                    response += f"- {cliente['cliente']}: ${cliente['total']:,.2f} MXN ({cliente['count']} facturas)\n"
                
                response += f"""
🔍 Data Sources Used
- facturas.xlsx: Cliente/Proveedor, Monto (MXN)

💡 Key Insights
- El cliente principal es {analysis['top_clientes'][0]['cliente']} con ${analysis['top_clientes'][0]['total']:,.2f} MXN
- Cantidad específica del cliente principal: ${analysis['top_clientes'][0]['total']:,.2f} pesos mexicanos
"""
                return response
        
        elif 'tipo' in question_lower or 'distribuyen' in question_lower:
            return f"""
📊 Executive Summary
Distribución de facturas por tipo: Por cobrar ${analysis['por_cobrar']:,.2f} MXN, Por pagar ${analysis['por_pagar']:,.2f} MXN

📈 Detailed Analysis
- Por cobrar: ${analysis['por_cobrar']:,.2f} MXN
- Por pagar: ${analysis['por_pagar']:,.2f} MXN
- Total: ${analysis['total']:,.2f} MXN

🔍 Data Sources Used
- facturas.xlsx: Tipo, Monto (MXN)

💡 Key Insights
- Las facturas por cobrar representan ${(analysis['por_cobrar']/analysis['total']*100):.1f}% del total
- Las facturas por pagar representan ${(analysis['por_pagar']/analysis['total']*100):.1f}% del total
- Cantidades específicas: Por cobrar ${analysis['por_cobrar']:,.2f} pesos, Por pagar ${analysis['por_pagar']:,.2f} pesos
"""
        
        return f"""
📊 Executive Summary
Análisis de facturas - Información general disponible

📈 Detailed Analysis
No pude procesar específicamente tu pregunta: "{question}"

💡 Preguntas que puedo responder sobre facturas:
- ¿Cuál es el total de facturas emitidas?
- ¿Cuál es el promedio de las facturas?
- ¿Cuáles son mis clientes principales?
- ¿Cómo se distribuyen las facturas por tipo?
- ¿Cuál es la factura por pagar más alta?
- ¿Cuál es la factura por pagar más baja?
- ¿Cuál es la factura por cobrar más alta?
- ¿Cuál es la factura por cobrar más baja?

🔍 Data Sources Available
- facturas.xlsx: Datos completos de facturas con tipo y montos
"""
    
    def answer_followup_question(self, question):
        """Responder preguntas de seguimiento sobre cantidades específicas."""
        question_lower = question.lower()
        
        if not self.last_analysis:
            return "No tengo información previa para responder esta pregunta de seguimiento."
        
        # Buscar cantidades específicas en el análisis anterior
        if 'por pagar' in question_lower and 'alta' in question_lower:
            if 'por_pagar_max' in self.last_analysis:
                return f"""
💰 Cantidad específica de la factura por pagar más alta:
${self.last_analysis['por_pagar_max']:,.2f} pesos mexicanos

📋 Detalles adicionales:
- Proveedor: {self.last_analysis.get('por_pagar_max_details', {}).get('proveedor', 'N/A')}
- Folio: {self.last_analysis.get('por_pagar_max_details', {}).get('folio', 'N/A')}
- Fecha: {self.last_analysis.get('por_pagar_max_details', {}).get('fecha', 'N/A')}
"""
        
        elif 'por cobrar' in question_lower and 'alta' in question_lower:
            if 'por_cobrar_max' in self.last_analysis:
                return f"""
💰 Cantidad específica de la factura por cobrar más alta:
${self.last_analysis['por_cobrar_max']:,.2f} pesos mexicanos

📋 Detalles adicionales:
- Cliente: {self.last_analysis.get('por_cobrar_max_details', {}).get('cliente', 'N/A')}
- Folio: {self.last_analysis.get('por_cobrar_max_details', {}).get('folio', 'N/A')}
- Fecha: {self.last_analysis.get('por_cobrar_max_details', {}).get('fecha', 'N/A')}
"""
        
        elif 'total' in question_lower:
            if 'total' in self.last_analysis:
                return f"""
💰 Cantidad específica del total de facturas:
${self.last_analysis['total']:,.2f} pesos mexicanos
"""
        
        elif 'promedio' in question_lower:
            if 'promedio' in self.last_analysis:
                return f"""
💰 Cantidad específica del promedio de facturas:
${self.last_analysis['promedio']:,.2f} pesos mexicanos
"""
        
        return f"""
❓ No pude identificar qué cantidad específica necesitas de mi análisis anterior.

💡 Puedes preguntar por:
- La cantidad de la factura por pagar más alta
- La cantidad de la factura por cobrar más alta  
- El total de facturas
- El promedio de facturas
- Cualquier otra cantidad que haya mencionado

🔍 Mi último análisis incluye: {list(self.last_analysis.keys())}
"""
    
    def answer_gastos_question(self, question):
        """Responder preguntas sobre gastos fijos."""
        analysis = self.analyze_gastos()
        
        if 'total' in question.lower():
            return f"""
📊 Executive Summary
Total de gastos fijos: ${analysis['total']:,.2f} MXN

📈 Detailed Analysis
- Total gastos fijos: ${analysis['total']:,.2f} MXN
- Número de gastos: {analysis['count']}
- Promedio por gasto: ${analysis['promedio']:,.2f} MXN

🔍 Data Sources Used
- gastos_fijos.xlsx: Gasto Fijo, Monto (MXN)

💡 Key Insights
- Total de gastos fijos mensuales: ${analysis['total']:,.2f} MXN
- Cantidad específica: ${analysis['total']:,.2f} pesos mexicanos
"""
        
        elif 'categoría' in question.lower() or 'distribuyen' in question.lower():
            response = f"""
📊 Executive Summary
Distribución de gastos fijos por categoría

📈 Detailed Analysis
"""
            for categoria in analysis['categorias']:
                response += f"- {categoria['Gasto Fijo']}: ${categoria['Monto (MXN)']:,.2f} MXN\n"
            
            response += f"""
🔍 Data Sources Used
- gastos_fijos.xlsx: Gasto Fijo, Monto (MXN)

💡 Key Insights
- El gasto más alto es {analysis['categorias'][0]['Gasto Fijo']} con ${analysis['categorias'][0]['Monto (MXN)']:,.2f} MXN
- Cantidad específica del gasto más alto: ${analysis['categorias'][0]['Monto (MXN)']:,.2f} pesos mexicanos
"""
            return response
        
        elif 'alto' in question.lower() or 'altos' in question_lower():
            response = f"""
📊 Executive Summary
Gastos fijos más altos: {analysis['categorias'][0]['Gasto Fijo']} con ${analysis['categorias'][0]['Monto (MXN)']:,.2f} MXN

📈 Detailed Analysis
Top 3 gastos más altos:
"""
            for i, categoria in enumerate(analysis['categorias'][:3], 1):
                response += f"- {categoria['Gasto Fijo']}: ${categoria['Monto (MXN)']:,.2f} MXN\n"
            
            response += f"""
🔍 Data Sources Used
- gastos_fijos.xlsx: Gasto Fijo, Monto (MXN)

💡 Key Insights
- El gasto más alto representa ${(analysis['categorias'][0]['Monto (MXN)']/analysis['total']*100):.1f}% del total
- Cantidad específica del gasto más alto: ${analysis['categorias'][0]['Monto (MXN)']:,.2f} pesos mexicanos
"""
            return response
        
        return "No pude analizar esa pregunta específica sobre gastos fijos."
    
    def answer_estado_question(self, question):
        """Responder preguntas sobre estado de cuenta."""
        analysis = self.analyze_estado_cuenta()
        
        if 'flujo' in question.lower() and 'caja' in question.lower():
            return f"""
📊 Executive Summary
Flujo de caja neto: ${analysis['neto']:,.2f} MXN

📈 Detailed Analysis
- Ingresos: ${analysis['ingresos']:,.2f} MXN
- Egresos: ${abs(analysis['egresos']):,.2f} MXN
- Flujo neto: ${analysis['neto']:,.2f} MXN
- Número de transacciones: {analysis['count']}

🔍 Data Sources Used
- Estado_cuenta.xlsx: Fecha, Descripción de la transacción, Monto de la transacción (MXN)

💡 Key Insights
- El flujo de caja es {'positivo' if analysis['neto'] > 0 else 'negativo'}
- Los ingresos representan ${(analysis['ingresos']/(analysis['ingresos']+abs(analysis['egresos']))*100):.1f}% del total de movimientos
- Cantidad específica del flujo neto: ${analysis['neto']:,.2f} pesos mexicanos
"""
        
        elif 'ingreso' in question.lower() or 'egreso' in question.lower():
            return f"""
📊 Executive Summary
Ingresos: ${analysis['ingresos']:,.2f} MXN, Egresos: ${abs(analysis['egresos']):,.2f} MXN

📈 Detailed Analysis
- Total ingresos: ${analysis['ingresos']:,.2f} MXN
- Total egresos: ${abs(analysis['egresos']):,.2f} MXN
- Diferencia: ${analysis['neto']:,.2f} MXN

🔍 Data Sources Used
- Estado_cuenta.xlsx: Monto de la transacción (MXN)

💡 Key Insights
- Los egresos son ${abs(analysis['egresos']/analysis['ingresos']):.1f}x mayores que los ingresos
- Cantidades específicas: Ingresos ${analysis['ingresos']:,.2f} pesos, Egresos ${abs(analysis['egresos']):,.2f} pesos
"""
        
        elif 'saldo' in question.lower():
            return f"""
📊 Executive Summary
Saldo actual de la cuenta bancaria: ${analysis['saldo_actual']:,.2f} MXN

📈 Detailed Analysis
- Saldo actual: ${analysis['saldo_actual']:,.2f} MXN
- Flujo neto: ${analysis['neto']:,.2f} MXN
- Total transacciones: {analysis['count']}

🔍 Data Sources Used
- Estado_cuenta.xlsx: Saldo (MXN)

💡 Key Insights
- El saldo actual es {'positivo' if analysis['saldo_actual'] > 0 else 'negativo'}
- Cantidad específica del saldo: ${analysis['saldo_actual']:,.2f} pesos mexicanos
"""
        
        return "No pude analizar esa pregunta específica sobre el estado de cuenta."
    
    def answer_combined_question(self, question):
        """Responder preguntas combinadas."""
        facturas_analysis = self.analyze_facturas()
        estado_analysis = self.analyze_estado_cuenta()
        
        return f"""
📊 Executive Summary
Análisis combinado de facturas por cobrar/pagar y flujo de caja

📈 Detailed Analysis
Facturas:
- Por cobrar: ${facturas_analysis['por_cobrar']:,.2f} MXN
- Por pagar: ${facturas_analysis['por_pagar']:,.2f} MXN

Flujo de caja:
- Ingresos: ${estado_analysis['ingresos']:,.2f} MXN
- Egresos: ${abs(estado_analysis['egresos']):,.2f} MXN
- Neto: ${estado_analysis['neto']:,.2f} MXN

🔍 Data Sources Used
- facturas.xlsx: Tipo, Monto (MXN)
- Estado_cuenta.xlsx: Monto de la transacción (MXN)

💡 Key Insights
- Las facturas por pagar superan a las por cobrar en ${facturas_analysis['por_pagar'] - facturas_analysis['por_cobrar']:,.2f} MXN
- El flujo de caja es {'positivo' if estado_analysis['neto'] > 0 else 'negativo'}
- Cantidades específicas: Por cobrar ${facturas_analysis['por_cobrar']:,.2f} pesos, Por pagar ${facturas_analysis['por_pagar']:,.2f} pesos
"""
    
    def answer_general_question(self, question):
        """Responder preguntas generales."""
        return f"""
📊 Executive Summary
Análisis general de datos financieros

📈 Detailed Analysis
No pude procesar específicamente tu pregunta: "{question}"

💡 Sugerencias de preguntas:
- ¿Cuál es el total de facturas emitidas?
- ¿Cuáles son mis gastos fijos más altos?
- ¿Cuál es mi flujo de caja?
- ¿Cómo se distribuyen las facturas por tipo?
- ¿Cuál es el saldo de mi cuenta bancaria?
- ¿Cuál es la factura por pagar más alta?
- ¿Cuál es la factura por cobrar más alta?

🔍 Data Sources Available
- facturas.xlsx: Datos de facturas
- gastos_fijos.xlsx: Gastos fijos mensuales
- Estado_cuenta.xlsx: Movimientos bancarios
"""


def main():
    """Función principal del agente interactivo."""
    print("🎯 FINANCIAL AGENT - INTERACTIVO")
    print("=" * 60)
    print("💡 Haz preguntas sobre tus datos financieros")
    print("📊 Ejemplos de preguntas:")
    print("   - ¿Cuál es el total de facturas emitidas?")
    print("   - ¿Cuáles son mis gastos fijos más altos?")
    print("   - ¿Cuál es mi flujo de caja?")
    print("   - ¿Cómo se distribuyen las facturas por tipo?")
    print("   - ¿Cuál es el saldo de mi cuenta bancaria?")
    print("   - ¿Cuál es la factura por pagar más alta?")
    print("   - ¿Cuál es la factura por cobrar más alta?")
    print("   - ¿Cómo variaron mis facturas por pagar y por cobrar?")
    print("   - ¿Cuál fue la cantidad en peso de la factura más alta?")
    print("=" * 60)
    
    agent = InteractiveFinancialAgent()
    
    while True:
        try:
            question = input("\n❓ Tu pregunta (o 'salir' para terminar): ").strip()
            
            if question.lower() in ['salir', 'exit', 'quit', 'q']:
                print("👋 ¡Hasta luego!")
                break
            
            if not question:
                continue
            
            print("\n" + "=" * 60)
            print(f"🔍 Procesando: {question}")
            print("=" * 60)
            
            response = agent.answer_question(question)
            print(response)
            
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Intenta con otra pregunta")


if __name__ == "__main__":
    main() 