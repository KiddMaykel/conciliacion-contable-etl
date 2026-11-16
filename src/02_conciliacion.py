import sqlite3
import pandas as pd
import os

print("🔄 Iniciando proceso de conciliación contable...")

# 1. EXTRACCIÓN (Extraer datos de SQLite y del archivo CSV)
# 1.1 Leer el Libro Mayor desde la base de datos SQLite
conn = sqlite3.connect('database/contabilidad.db')
query = "SELECT id_asiento, fecha, glosa, cuenta_contable, monto FROM libro_mayor"
df_erp = pd.read_sql(query, conn)
conn.close()

# 1.2 Leer la Cartola Bancaria desde el archivo CSV
df_banco = pd.read_csv('data/raw/cartola_banco_oct2026.csv')

print(f"📊 Registros en ERP extraídos: {len(df_erp)}")
print(f"📊 Registros en Banco extraídos: {len(df_banco)}")

# 2. TRANSFORMACIÓN Y CRUCE DE DATOS (Matching)
# Haremos un Full Outer Join basado en el monto para encontrar coincidencias y diferencias
df_conciliacion = pd.merge(
    df_erp, 
    df_banco, 
    left_on='monto', 
    right_on='monto', 
    how='outer', 
    suffixes=('_erp', '_banco')
)

# 3. CLASIFICACIÓN DE ESTADOS (Auditoría automática)
def clasificar_estado(row):
    if pd.notna(row['id_asiento']) and pd.notna(row['id_trx_banco']):
        return 'Conciliado OK'
    elif pd.notna(row['id_asiento']) and pd.isna(row['id_trx_banco']):
        return 'Solo en ERP (Pendiente de cobro/pago)'
    else:
        return 'Solo en Banco (No contabilizado / Comisión)'

df_conciliacion['estado_conciliacion'] = df_conciliacion.apply(clasificar_estado, axis=1)

# Limpiar y ordenar columnas para el reporte final
df_reporte = df_conciliacion[[
    'id_asiento', 'fecha_erp', 'glosa', 'monto', 
    'id_trx_banco', 'fecha_banco', 'descripcion', 'estado_conciliacion'
]].copy()

# 4. CARGA / EXPORTACIÓN (Guardar reporte final en Excel)
os.makedirs('data/output', exist_ok=True)
output_path = 'data/output/reporte_conciliacion_oct2026.xlsx'

df_reporte.to_excel(output_path, index=False)

print(f"✅ ¡Conciliación finalizada con éxito!")
print(f"📁 Reporte de auditoría generado en: {output_path}")